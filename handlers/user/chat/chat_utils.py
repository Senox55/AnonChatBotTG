from aiogram import Router, Bot
from aiogram.types import Message
import json

from database.database import Database
from language.translator import Translator


async def close_game_after_stop_dialog(message: Message, db: Database, translator: Translator, bot: Bot):
    user_id_one = message.chat.id
    chat_info = await db.get_active_chat(user_id_one)
    user_id_two = chat_info[1]
    await db.increment_chat_count(user_id_one)
    await db.increment_chat_count(user_id_two)

    user_state_one = await db.get_user_state(user_id_one)

    if user_state_one:
        user_data_one = json.loads(user_state_one['data'])

        user_one_message_id = user_data_one.get('message_id')

        await bot.edit_message_text(
            chat_id=user_id_one,
            message_id=user_one_message_id,
            text=translator.get('game_close_player')
        )
    await db.clear_user_state(user_id_one)
    await db.delete_chat(chat_info[0])
