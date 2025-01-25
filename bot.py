import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import load_config
from database.utils import get_pg_pool
from language.translator import Translator
from middlewares import VipCheckMiddleware, CheckValidityVipMiddleware, RegistrationCheckMiddleware, \
    TranslatorMiddleware, DataBaseMiddleware
from handlers import vip_router, user_router


async def main():
    # Загружаем конфиги
    config = load_config('.env')

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=MemoryStorage())

    # Databese pool
    db_pool = await get_pg_pool(
        db_name=config.db.database,
        host=config.db.db_host,
        port=config.db.db_port,
        user=config.db.db_user,
        password=config.db.db_password
    )

    # Регистрация routers
    dp.include_router(vip_router)
    dp.include_router(user_router)

    # Регистрация middlewares
    dp.update.middleware(DataBaseMiddleware())
    dp.update.middleware(TranslatorMiddleware())
    dp.message.middleware(RegistrationCheckMiddleware())
    dp.message.middleware(CheckValidityVipMiddleware())
    vip_router.message.middleware(VipCheckMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot,
                               _db_pool=db_pool,
                               translator=Translator())
    finally:
        await db_pool.close()


if __name__ == '__main__':
    asyncio.run(main())
