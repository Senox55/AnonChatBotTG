import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import load_config
from database.utils import get_pg_pool
from language.translator import Translator
from middlewares import VipCheckMiddleware, CheckValidityVipMiddleware, RegistrationCheckMiddleware, \
    TranslatorMiddleware, DataBaseMiddleware
from handlers import vip_router, user_router

logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting bot")
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
    vip_router.callback_query.middleware(VipCheckMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await asyncio.gather(
            dp.start_polling(
                bot,
                _db_pool=db_pool,
                translator=Translator()
            )
        )
    except Exception as e:
        logger.exception(e)
    finally:
        await db_pool.close()
        logger.info('Connection to Postgres closed')
