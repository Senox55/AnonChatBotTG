import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import Redis, RedisStorage
import redis

from config_data.config import load_config
from app.infrastructure.database.utils import get_pg_pool
from app.infrastructure.cache.utils.connect_to_redis import get_redis_pool
from locales.translator import Translator
from app.tgbot.middlewares import RegistrationCheckMiddleware, \
    TranslatorMiddleware, DataBaseMiddleware, RedisMiddleware
from app.tgbot.handlers import vip_router, user_router

logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting bot")
    # Загружаем конфиги
    config = load_config('../../.env')

    redis_client = Redis(host="localhost", decode_responses=True)

    storage = RedisStorage(redis=redis_client)

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)

    cache_pool: redis.asyncio.Redis = await get_redis_pool(
        db=config.redis.database,
        host=config.redis.host,
        port=config.redis.port
    )
    dp.workflow_data.update(_cache_pool=cache_pool)

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
    dp.update.middleware(RedisMiddleware())
    dp.update.middleware(TranslatorMiddleware())
    dp.message.middleware(RegistrationCheckMiddleware())
    # dp.message.middleware(CheckValidityVipMiddleware())
    # vip_router.message.middleware(VipCheckMiddleware())
    # vip_router.callback_query.middleware(VipCheckMiddleware())

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
        if dp.workflow_data.get('_cache_pool'):
            await cache_pool.close()
            logger.info('Connection to Redis closed')
