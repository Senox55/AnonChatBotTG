from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from database import Database
from config import bot_token

BOT_TOKEN = bot_token

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

db = Database()

button_start_search = KeyboardButton(text='😎 Поиск собеседника')
button_stop_search = KeyboardButton(text='❌ Остановить поиск собеседника')
button_stop_dialog = KeyboardButton(text='Остановить диалог')

keyboard_before_start_search = ReplyKeyboardMarkup(keyboard=[[button_start_search]], resize_keyboard=True)
keyboard_after_start_research = ReplyKeyboardMarkup(keyboard=[[button_stop_search]], resize_keyboard=True)
keyboard_after_find_dialog = ReplyKeyboardMarkup(keyboard=[[button_stop_dialog]], resize_keyboard=True)


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        'Добро пожаловать в анонимный чат бот!\n'
        'Чтобы начать общение нажмите кнопку '
        '"Поиск собеседника"',
        reply_markup=keyboard_before_start_search
    )


@dp.message(F.text == 'Остановить диалог')
async def process_stop_dialog(message: Message):
    chat_info = await db.get_active_chat(message.chat.id)
    print(chat_info)
    if chat_info:
        await db.delete_chat(chat_info[0])
        await bot.send_message(
            message.chat.id,
            "Вы покинули чат",
            reply_markup=keyboard_before_start_search,
        )
        await bot.send_message(
            chat_info[1],
            "Собеседник покинул чат",
            reply_markup=keyboard_before_start_search
        )
    else:
        await message.answer(
            'Вы не находитесь в диалоге',
            reply_markup=keyboard_before_start_search
        )


@dp.message(F.text == '😎 Поиск собеседника')
async def process_start_search_command(message: Message):
    chat_two = await db.get_chat()  # берем собеседника, который стоит первый в очереди
    if not await(db.create_chat(message.chat.id, chat_two)):
        await db.add_queue(message.chat.id)
        await message.answer(
            'Ищем собеседника...',
            reply_markup=keyboard_after_start_research
        )

    else:
        mess = "Собеседник найден!,\nЧтобы остановить диалог напишите /stop"
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


@dp.message(F.text == '❌ Остановить поиск собеседника')
async def process_finish_search_command(message: Message):
    # Проверяем, находится ли пользователь в очереди
    is_in_queue = await db.is_in_queue(message.chat.id)
    print(is_in_queue)

    if is_in_queue:
        # Удаляем пользователя из очереди, если он в поиске
        await db.delete_queue(message.chat.id)
        await message.answer(
            'Поиск отменён',
            reply_markup=keyboard_before_start_search
        )
    else:
        # Уведомляем, что пользователь не в поиске
        await message.answer(
            'Вы не находитесь в поиске.',
            reply_markup=keyboard_before_start_search
        )


@dp.message()
async def process_chatting(message: Message):
    chat_info = await db.get_active_chat(message.chat.id)
    print(chat_info)
    if chat_info:
        await message.send_copy(chat_id=chat_info[1])
    else:
        await message.answer(
            'Вы еще не начали диалог',
            reply_markup=keyboard_before_start_search
        )


if __name__ == '__main__':
    dp.run_polling(bot)
