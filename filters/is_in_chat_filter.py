from aiogram.filters import Filter
from aiogram import types
import logging

from aiogram.types import CallbackQuery


class IsINChat(Filter):
    async def __call__(self, callback: CallbackQuery, db) -> bool:
        user_id = callback.from_user.id
        chat_info = await db.get_active_chat(user_id)
        if chat_info:
            return True  # Чат есть

        # Если чата нет, возвращаем False
        return False
