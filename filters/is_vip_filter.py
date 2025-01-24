from aiogram.filters import Filter
from aiogram.types import Message
import logging

from database.database import Database
from language.translator import Translator
from keyboards import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class IsVIP(Filter):
    async def __call__(self, message: Message, db: Database, translator: Translator) -> bool:
        """
        Функция для проверки, является ли пользователь випом
        :param message:
        :param db:
        :return:
        """
        user_id = message.chat.id
        vip_status = await db.get_vip_status(user_id)
        if vip_status:
            return True  # Статус активен

        # Если статуса нет, возвращаем False
        await message.answer(
            text=translator.get('vip_description'),
            reply_markup=buy_vip_keyboard_inline)
        return False
