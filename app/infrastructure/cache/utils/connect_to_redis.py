import logging
import redis

from redis.asyncio import ConnectionPool, Redis

logger = logging.getLogger(__name__)


async def get_redis_pool(
        db: str,
        host: str,
        port: int
) -> redis.asyncio.Redis:
    pool = ConnectionPool(
        host=host, port=port, db=db, decode_responses=True
    )
    redis_pool: redis.asyncio.Redis = Redis(
        connection_pool=pool
    )

    return redis_pool
