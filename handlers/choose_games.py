from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
import logging
import json

from keyboards import *
from filters.is_in_chat_filter import IsINChat

logging.basicConfig(level=logging.INFO)

router = Router()


async def process_choose_game(message: Message, db, translator):
    user_id = message.chat.id
    chat_info = await db.get_active_chat(user_id)

    user_state_info = await db.get_user_state(user_id)
    if user_state_info:
        user_state = user_state_info['state']

        if user_state in ["waiting_for_opponent", "waiting_for_start", "playing", "player1_turn", "player2_turn"]:
            await message.answer(
                translator.get('start_play_when_in_game'),
                reply_markup=keyboard_after_find_dialog)
            return
    else:
        logging.info(f"user {user_id} choose game")
        user_one_message = await message.answer(
            text=translator.get('choose_game'),
            reply_markup=keyboard_before_choose_game_inline
        )

        await db.set_user_state(user_id, "waiting_for_opponent", json.dumps({"message_id": user_one_message.message_id}))


@router.message(Command(commands=['play']), IsINChat())
async def process_choose_game_command(message: Message, db, translator):
    await process_choose_game(message, db, translator)


@router.message(F.text == '🎲 Сыграть в игру', IsINChat())
async def process_choose_game_button(message: Message, db, translator):
    await process_choose_game(message, db, translator)
