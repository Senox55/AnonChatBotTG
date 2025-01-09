from aiogram import F, Router
from aiogram.types import Message

from keyboards import *

router = Router()


@router.message(F.text == '✋ Остановить поиск')
async def process_finish_search_command(message: Message, db):
    # Проверяем, находится ли пользователь в очереди
    is_in_queue = await db.is_in_queue(message.chat.id)

    if is_in_queue:
        # Удаляем пользователя из очереди, если он в поиске
        await db.delete_queue(message.chat.id)
        await message.answer(
            'Поиск отменён',
            reply_markup=keyboard_before_start_search
        )
    else:
        # Уведомляем, что пользователь не в поиске
        await message.answer(
            'Вы не находитесь в поиске.',

            reply_markup=keyboard_before_start_search
        )
