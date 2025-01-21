from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
import logging
import json

from keyboards import *
from filters.is_in_chat_filter import IsINChat

logging.basicConfig(level=logging.INFO)

router = Router()


@router.message(Command(commands=['play']), IsINChat())
async def process_choose_game_command(message: Message, db, translator):
    user_id = message.chat.id
    chat_info = await db.get_active_chat(user_id)

    user_state_info = await db.get_user_state(user_id)
    if user_state_info:
        user_state = user_state_info['state']

        if user_state in ["waiting_for_opponent", "waiting_for_start", "playing", "player1_turn", "player2_turn"]:
            await message.answer(
                translator.get('start_play_when_in_game'))
            return
    else:
        await db.set_user_state(user_id, "waiting_for_opponent")

    if chat_info:
        logging.info(f"user {user_id} choose game")
        await message.answer(
            text=translator.get('choose_game'),
            reply_markup=keyboard_before_choose_game_inline
        )
    else:
        await message.answer(
            translator.get('when_not_in_dialog'),
            reply_markup=keyboard_before_start_search)
