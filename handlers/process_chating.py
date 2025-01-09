from aiogram import Dispatcher, Router
from aiogram.types import Message

from keyboards import *

router = Router()


@router.message()
async def process_chatting(message: Message, db):

    chat_info = await db.get_active_chat(message.chat.id)
    is_in_queue = await db.is_in_queue(message.chat.id)
    if chat_info:
        await message.send_copy(chat_id=chat_info[1])
    elif is_in_queue:
        await message.answer(
            'Вы уже находитесь в поиске 🕵️‍♂️.\n'
            'Пожалуйста, немного подождите, пока мы найдем для вас собеседника. ⏳\n\n'
            'Если хотите отменить поиск, нажмите "✋ Остановить поиск" или отправьте /stop.',
            reply_markup=keyboard_after_start_research
        )
    else:
        await message.answer(
            'Вы еще не начали диалог',
            reply_markup=keyboard_before_start_search
        )


