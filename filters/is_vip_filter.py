from aiogram.filters import Filter
from aiogram import types
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class IsVIP(Filter):
    async def __call__(self, message: types.Message, db) -> bool:
        user_id = message.chat.id
        vip_status = await db.get_vip_status(user_id)
        if vip_status:
            return True  # Статус активен

        # Если статуса нет, возвращаем False
        return False
