from aiogram import Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command


from keyboards import *

router = Router()


async def increment_chat_count(user_id: int, db):
    await db.increment_chat_count(user_id)


async def stop_dialog(message: Message, db, bot):
    chat_info = await db.get_active_chat(message.chat.id)
    if chat_info:
        await increment_chat_count(message.chat.id)
        await increment_chat_count(chat_info[1])

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
    else:
        is_in_queue = await db.is_in_queue(message.chat.id)
        if is_in_queue:
            await db.delete_queue(message.chat.id)
            await message.answer(
                '🔕 Поиск отменён.',
                reply_markup=keyboard_before_start_search
            )
        else:
            await message.answer(
                '⚠ Вы не находитесь в диалоге.\n'
                'Напишите /search, чтобы найти собеседника',
                reply_markup=keyboard_before_start_search
            )


@router.message(Command(commands=['stop']))
async def process_stop_command(message: Message):
    await stop_dialog(message)


@router.message(F.text == '❌ Завершить диалог')
async def process_stop_button(message: Message):
    await stop_dialog(message)


