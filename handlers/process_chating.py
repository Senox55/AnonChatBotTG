from aiogram import Router
from aiogram.types import Message

from keyboards import *

router = Router()


@router.message()
async def process_chatting(message: Message, db, translator):

    chat_info = await db.get_active_chat(message.chat.id)
    is_in_queue = await db.is_in_queue(message.chat.id)
    if chat_info:
        await message.send_copy(chat_id=chat_info[1])
    elif is_in_queue:
        await message.answer(
            translator.get('start_search_when_in_search'),
            reply_markup=keyboard_after_start_research
        )
    else:
        await message.answer(
            translator.get('when_not_in_dialog'),
            reply_markup=keyboard_before_start_search
        )


