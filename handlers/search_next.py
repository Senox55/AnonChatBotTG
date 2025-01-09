from aiogram import Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command

from keyboards import *

router = Router()


@router.message(Command(commands=['next']))
async def process_next_command(message: Message, db, bot, desired_gender='anon'):
    chat_info = await db.get_active_chat(message.chat.id)
    if chat_info:
        await db.delete_chat(chat_info[0])
        await bot.send_message(
            message.chat.id,
            "Вы покинули чат ❌",
            reply_markup=keyboard_before_start_search,
        )
        await bot.send_message(
            chat_info[1],
            "Ваш собеседник завершил диалог ❌",
            reply_markup=keyboard_before_start_search
        )

    user_info = await db.get_chat(desired_gender)
    chat_two = user_info[0]
    gender = user_info[1]
    desired_gender_of_other = user_info[2]  # Пол, который ищет другой пользователь

    is_in_queue = await db.is_in_queue(message.chat.id)

    if not is_in_queue:
        if (message.chat.id == chat_two
                or user_info == [0]
                or (desired_gender_of_other != 'anon' and await db.get_gender(
                    message.chat.id) != desired_gender_of_other)
                or not await db.create_chat(message.chat.id, chat_two)):

            await db.add_queue(message.chat.id, await db.get_gender(message.chat.id), desired_gender)
            await message.answer(
                'Ищем собеседника... 🔍\n\n'
                'Пожалуйста, подождите немного — мы уже подбираем для вас интересного человека. 😊',
                reply_markup=keyboard_after_start_research
            )
        else:
            mess = '''🎉 Ура! Собеседник найден! \n\nНачинайте общение прямо сейчас.\n/next — искать нового собеседника\n/stop — закончить диалог'''
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
            'Вы уже находитесь в поиске 🕵️‍♂️.\n'
            'Пожалуйста, немного подождите, пока мы найдем для вас собеседника. ⏳\n\n'
            'Если хотите отменить поиск, нажмите "✋ Остановить поиск" или отправьте /stop.',
            reply_markup=keyboard_after_start_research
        )

