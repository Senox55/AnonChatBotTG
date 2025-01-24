from aiogram import Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import Message
import logging
import json

from handlers.stop_dialog import increment_chat_count
from keyboards import *

router = Router()


@router.message()
async def process_chatting(message: Message, db, translator, bot):
    user_id_one = message.chat.id
    chat_info = await db.get_active_chat(message.chat.id)
    is_in_queue = await db.is_in_queue(message.chat.id)

    if chat_info:
        try:
            await message.send_copy(chat_id=chat_info[1])
        except TelegramForbiddenError:
            logging.info(TelegramForbiddenError)
            await increment_chat_count(message.chat.id, db)
            await increment_chat_count(chat_info[1], db)

            user_state_one = await db.get_user_state(user_id_one)

            if user_state_one:
                user_data_one = json.loads(user_state_one['data'])

                user_one_message_id = user_data_one.get('message_id')

                await bot.edit_message_text(
                    chat_id=user_id_one,
                    message_id=user_one_message_id,
                    text="Игра завершена. Вы покинули чат."
                )
            await db.clear_user_state(user_id_one)
            await db.delete_chat(chat_info[0])
            await message.answer(translator.get('interlocutor_blocked_bot'), reply_markup=keyboard_before_start_search)
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
