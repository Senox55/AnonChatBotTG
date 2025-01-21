from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import logging

from keyboards import *

router = Router()
logging.basicConfig(level=logging.INFO)


@router.message(Command(commands=['next']))
async def process_next_command(message: Message, db, bot, translator):
    user_id = message.chat.id
    chat_info = await db.get_active_chat(user_id)

    preferred_gender = await db.get_preferred_gender(user_id)
    logging.info(f"User {user_id} have preferred gender = {preferred_gender}")
    if chat_info:
        await db.delete_chat(chat_info[0])
        await bot.send_message(
            user_id,
            translator.get('evaluate_interlocutor'),
            reply_markup=keyboard_evaluate_interlocutor
        )
        await bot.send_message(
            chat_info[1],
            translator.get('interlocutor_stop_dialog'),
            reply_markup=keyboard_before_start_search
        )

        await bot.send_message(
            chat_info[1],
            translator.get('evaluate_interlocutor'),
            reply_markup=keyboard_evaluate_interlocutor
        )

    is_in_queue = await db.is_in_queue(user_id)
    chat_info = await db.get_active_chat(user_id)

    chat_two = await db.get_chat(await db.get_gender(user_id), preferred_gender)

    if not is_in_queue:
        if not chat_info:
            if not await db.create_chat(user_id, chat_two):
                await db.add_queue(user_id)

            else:
                mess = translator.get('found_interlocutor')
                await bot.send_message(
                    user_id,
                    mess,
                    reply_markup=keyboard_after_find_dialog
                )
                await bot.send_message(
                    chat_two,
                    mess,
                    reply_markup=keyboard_after_find_dialog
                )
        else:
            await message.answer(
                translator.get('start_search_when_in_dialog'),
                reply_markup=keyboard_after_find_dialog
            )

    else:
        await message.answer(
            translator.get('start_search_when_in_search'),
            reply_markup=keyboard_after_start_research
        )
