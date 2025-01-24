from aiogram.filters import Filter
from aiogram.types import CallbackQuery
import asyncpg
import logging


class DBStateFilter(Filter):
    def __init__(self, state: str):
        self.state = state

    async def __call__(self, callback: CallbackQuery, db: asyncpg.Pool) -> bool:
        """
        Функция для проверки состояния пользователя в базе данных
        :param callback:
        :param db:
        :return:
        """
        user_id = callback.from_user.id
        state_info = await db.get_user_state(user_id)
        if state_info:
            return self.state == state_info['state']
        return False
