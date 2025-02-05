from typing import Awaitable, Callable, Dict, Any
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject

class RedisMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        redis_pool = data["_cache_pool"]
        data["redis"] = redis_pool
        return await handler(event, data)