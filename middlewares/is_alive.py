from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

import logging

logging.basicConfig(level=logging.INFO)


class IsAliveCheckMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        db = data["db"]

        user_id = event.chat.id

        is_alive = await db.is_alive(user_id)
        logging.info(f"Пользователь {user_id} имеет статут is_alive={is_alive}")
        if is_alive:
            return await handler(event, data)
