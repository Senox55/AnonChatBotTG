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

        # Список разрешенных команд для незарегистрированных пользователей
        allowed_commands = ["Я Парень 🙋‍♂️", "Я Девушка 🙋‍♀️", '📍 До 17', '📍 18-21', '📍 22-25', '📍 26-35', '📍 36-45',
                            '📍 46+']

        # Проверяем, является ли сообщение командой и разрешена ли она
        if event.text in (allowed_commands):
            return await handler(event, data)

        user_id = event.chat.id

        is_alive = await db.is_alive(user_id)
        logging.info(f"Пользователь {user_id} имеет статут is_alive={is_alive}")
        if is_alive:
            return await handler(event, data)
