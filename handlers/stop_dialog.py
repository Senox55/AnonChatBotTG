from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
import json

from keyboards import *

router = Router()


async def increment_chat_count(user_id: int, db):
    await db.increment_chat_count(user_id)


async def stop_dialog(message: Message, db, bot, translator, from_search_next=False):
    user_id_one = message.from_user.id

    chat_info = await db.get_active_chat(user_id_one)

    if chat_info:
        await increment_chat_count(message.chat.id, db)
        await increment_chat_count(chat_info[1], db)

        user_state_one = await db.get_user_state(user_id_one)

        user_id_two = chat_info[1]
        user_state_two = await db.get_user_state(user_id_two)
        if user_state_one:
            user_data_one = json.loads(user_state_one['data'])

            user_one_message_id = user_data_one.get('message_id')

            await bot.edit_message_text(
                chat_id=user_id_one,
                message_id=user_one_message_id,
                text="Игра завершена. Вы покинули чат."
            )

        if user_state_two:
            user_data_two = json.loads(user_state_two['data'])

            user_two_message_id = user_data_two.get('message_id')

            await bot.edit_message_text(
                chat_id=user_id_two,
                message_id=user_two_message_id,
                text="Игра завершена. Собеседник покинул чат."
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

        await bot.send_message(
            chat_info[1],
            translator.get('interlocutor_stop_dialog'),
            reply_markup=keyboard_before_start_search)

        await bot.send_message(
            chat_info[1],
            translator.get('evaluate_interlocutor'),
            reply_markup=keyboard_evaluate_interlocutor
        )

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
async def process_stop_command(message: Message, db, bot, translator):
    await stop_dialog(message, db, bot, translator)


@router.message(F.text == '👋 Завершить чат')
async def process_stop_button(message: Message, db, bot, translator):
    await stop_dialog(message, db, bot, translator)
