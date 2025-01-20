from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import logging

from keyboards import *

router = Router()
logging.basicConfig(level=logging.INFO)


@router.message(Command(commands=['next']))
async def process_next_command(message: Message, db, bot, translator, desired_gender='anon'):
    chat_info = await db.get_active_chat(message.chat.id)
    user_id = message.chat.id
    desired_gender = await db.get_desired_gender(user_id)
    logging.info(f"User {user_id} have desired gender = {desired_gender}")
    if chat_info:
        await db.delete_chat(chat_info[0])
        await bot.send_message(
            message.chat.id,
            translator.get('stop_dialog'),
            reply_markup=keyboard_before_start_search,
        )
        await bot.send_message(
            chat_info[1],
            translator.get('interlocutor_stop_dialog'),
            reply_markup=keyboard_before_start_search
        )

    is_in_queue = await db.is_in_queue(message.chat.id)
    chat_info = await db.get_active_chat(message.chat.id)

    chat_two = await db.get_chat(await db.get_gender(message.chat.id), desired_gender)

    if not is_in_queue:
        if not chat_info:
            if not await db.create_chat(message.chat.id, chat_two):

                await db.add_queue(message.chat.id, await db.get_gender(message.chat.id), desired_gender)
                if desired_gender == 'm':
                    search_message = translator.get('start_search_male')
                elif desired_gender == 'f':
                    search_message = translator.get('start_search_female')
                else:
                    search_message = translator.get('start_search')
                await message.answer(
                    search_message,
                    reply_markup=keyboard_after_start_research
                )
            else:
                mess = translator.get('found_interlocutor')
                await bot.send_message(
                    message.chat.id,
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
