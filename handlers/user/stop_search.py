from aiogram import F, Router
from aiogram.types import Message

from database.database import Database
from keyboards import *
from language.translator import Translator

router = Router()


@router.message(F.text == '✋ Отменить поиск')
async def process_finish_search_command(message: Message, db: Database, translator: Translator):
    # Проверяем, находится ли пользователь в очереди
    is_in_queue = await db.is_in_queue(message.chat.id)

    if is_in_queue:
        # Удаляем пользователя из очереди, если он в поиске
        await db.delete_queue(message.chat.id)
        await message.answer(
            translator.get('stop_search'),
            reply_markup=keyboard_before_start_search
        )
    else:
        # Уведомляем, что пользователь не в поиске
        await message.answer(
            translator.get('stop_search_when_bot_in_search'),

            reply_markup=keyboard_before_start_search
        )
