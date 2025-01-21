import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import load_config
from database.utils import get_pg_pool
from language.translator import Translator
from middlewares.database import DataBaseMiddleware
from middlewares.registration import RegistrationCheckMiddleware
from middlewares.translator import TranslatorMiddleware
from middlewares.vip_checker import VipCheckMiddleware
from middlewares.is_alive import IsAliveCheckMiddleware
from handlers import (start_search, stop_search, search_next, stop_dialog, profile, process_chating, registration,
                      edit_profile, buy_vip, block_bot, choose_games, game_xo, invite_games, reputation_system,
                      report_system)


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

    # Иницализация middlewares
    dp.update.middleware(DataBaseMiddleware())
    dp.update.middleware(TranslatorMiddleware())
    dp.message.middleware(RegistrationCheckMiddleware())
    dp.message.middleware(IsAliveCheckMiddleware())
    dp.message.middleware(VipCheckMiddleware())

    # Иницализация routers
    dp.include_router(block_bot.router)
    dp.include_router(registration.router)
    dp.include_router(buy_vip.router)
    dp.include_router(profile.router)
    dp.include_router(edit_profile.router)
    dp.include_router(start_search.router)
    dp.include_router(stop_search.router)
    dp.include_router(search_next.router)
    dp.include_router(stop_dialog.router)
    dp.include_router(reputation_system.router)
    dp.include_router(report_system.router)
    dp.include_router(choose_games.router)
    dp.include_router(invite_games.router)
    dp.include_router(game_xo.router)
    dp.include_router(process_chating.router)

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot,
                               _db_pool=db_pool,
                               translator=Translator())
    finally:
        await db_pool.close()


if __name__ == '__main__':
    asyncio.run(main())
