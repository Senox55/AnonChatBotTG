from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramForbiddenError
import logging
import json

from database.database import Database
from keyboards import *
from language.translator import Translator

router = Router()


async def stop_dialog(message: Message, db: Database, bot: Bot, translator: Translator, from_search_next=False):
    user_id_one = message.from_user.id

    chat_info = await db.get_active_chat(user_id_one)

    if chat_info:
        await db.increment_chat_count(message.chat.id)
        await db.increment_chat_count(chat_info[1])

        user_state_one = await db.get_user_state(user_id_one)

        user_id_two = chat_info[1]
        user_state_two = await db.get_user_state(user_id_two)
        if user_state_one:
            user_data_one = json.loads(user_state_one['data'])

            user_one_message_id = user_data_one.get('message_id')

            await bot.edit_message_text(
                chat_id=user_id_one,
                message_id=user_one_message_id,
                text=translator.get('game_close_player')
            )

        if user_state_two:
            user_data_two = json.loads(user_state_two['data'])

            user_two_message_id = user_data_two.get('message_id')

            await bot.edit_message_text(
                chat_id=user_id_two,
                message_id=user_two_message_id,
                text=translator.get('game_close_interlocutor')
            )

        await db.clear_user_state(message.chat.id)
        await db.clear_user_state(chat_info[1])

        await bot.send_message(
            message.chat.id,
            translator.get('stop_dialog'),
            reply_markup=keyboard_before_start_search,
        )

        await bot.send_message(
            message.chat.id,
            translator.get('evaluate_interlocutor'),
            reply_markup=keyboard_evaluate_interlocutor
        )

        try:
            await bot.send_message(
                chat_id=user_id_two,
                text=translator.get('interlocutor_stop_dialog'),
                reply_markup=keyboard_before_start_search
            )
            await bot.send_message(
                chat_id=user_id_two,
                text=translator.get('evaluate_interlocutor'),
                reply_markup=keyboard_evaluate_interlocutor
            )
        except TelegramForbiddenError:
            # Если пользователь 2 заблокировал бота
            logging.warning(f"Пользователь {user_id_two} заблокировал бота.")

        await db.delete_chat(chat_info[0])

    elif not from_search_next:
        is_in_queue = await db.is_in_queue(message.chat.id)
        if is_in_queue:
            await db.delete_queue(message.chat.id)
            await message.answer(
                translator.get('stop_search'),
                reply_markup=keyboard_before_start_search
            )
        else:
            await message.answer(
                translator.get('when_not_in_dialog'),
                reply_markup=keyboard_before_start_search
            )


@router.message(Command(commands=['stop']))
async def process_stop_command(message: Message, db: Database, bot: Bot, translator: Translator):
    await stop_dialog(message, db, bot, translator)


@router.message(F.text == '👋 Завершить чат')
async def process_stop_button(message: Message, db: Database, bot: Bot, translator: Translator):
    await stop_dialog(message, db, bot, translator)
