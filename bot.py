from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from database import Database
from config import bot_token
from functools import wraps

BOT_TOKEN = bot_token

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

db = Database()

button_search_random = KeyboardButton(text='Рандом 👫')
button_stop_search = KeyboardButton(text='✋ Остановить поиск')
button_stop_dialog = KeyboardButton(text='❌ Завершить диалог')
button_set_male = KeyboardButton(text='Я Парень 🙋‍♂️')
button_set_female = KeyboardButton(text='Я Девушка 🙋‍♀️')
button_search_male = KeyboardButton(text='Найти Парня 🙋‍♂️')
button_search_female = KeyboardButton(text='Найти Девушку 🙋‍♀️')

keyboard_before_start_search = ReplyKeyboardMarkup(
    keyboard=[[button_search_male, button_search_random, button_search_female]], resize_keyboard=True)
keyboard_after_start_research = ReplyKeyboardMarkup(keyboard=[[button_stop_search]], resize_keyboard=True)
keyboard_after_find_dialog = ReplyKeyboardMarkup(keyboard=[[button_stop_dialog]], resize_keyboard=True)
keyboard_before_set_gender = ReplyKeyboardMarkup(keyboard=[[button_set_male, button_set_female]], resize_keyboard=True)


def gender_required(func):
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        setted_gender = await db.get_gender(message.chat.id)
        if not setted_gender:
            await message.answer(
                'Для начала работы укажите ваш пол: ',
                reply_markup=keyboard_before_set_gender
            )
            return
        return await func(message, *args, **kwargs)

    return wrapper


async def start_search(message: Message, desired_gender: str = 'anon'):
    """
    Универсальная функция для начала поиска собеседника.

    :param message: Объект сообщения пользователя.
    :param desired_gender: Пол собеседника, которого ищет пользователь ('male', 'female', 'anon').
    """
    user_info = await db.get_chat(desired_gender)
    chat_two = user_info[0]
    gender = user_info[1]
    desired_gender_of_other = user_info[2]  # Пол, который ищет другой пользователь

    is_in_queue = await db.is_in_queue(message.chat.id)
    chat_info = await db.get_active_chat(message.chat.id)

    if not is_in_queue:
        if not chat_info:
            if (message.chat.id == chat_two
                    or user_info == [0]
                    or (desired_gender_of_other != 'anon' and await db.get_gender(
                        message.chat.id) != desired_gender_of_other)
                    or not await db.create_chat(message.chat.id, chat_two)):

                await db.add_queue(message.chat.id, await db.get_gender(message.chat.id), desired_gender)
                await message.answer(
                    'Ищем собеседника... 🔍',
                    reply_markup=keyboard_after_start_research
                )
            else:
                mess = "🎉 Собеседник найден!\n\nЧтобы завершить диалог, нажмите кнопку '❌ Завершить диалог' или отправьте команду /stop."
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
                "У вас уже есть собеседник 🤔\n/next — искать нового собеседника\n/stop — закончить диалог",
                reply_markup=keyboard_after_find_dialog
            )

    else:
        await message.answer(
            "Вы уже находитесь в поиске 🕵️‍♂️. Пожалуйста, подождите немного ⏳.\n\n"
            "Если хотите отменить поиск, просто нажмите '✋ Остановить поиск' или отправьте команду /stop.",
            reply_markup=keyboard_after_start_research
        )


@dp.message(CommandStart())
@gender_required
async def process_start_command(message: Message):
    await start_search(message, desired_gender='anon')


@dp.message(Command(commands=['search']))
@gender_required
async def process_start_command(message: Message):
    await start_search(message, desired_gender='anon')


@dp.message(F.text == 'Рандом 👫')
@gender_required
async def process_start_search_random_command(message: Message):
    await start_search(message, desired_gender='anon')


@dp.message(F.text == 'Найти Парня 🙋‍♂️')
@gender_required
async def process_start_search_male_command(message: Message):
    await start_search(message, desired_gender='male')


@dp.message(F.text == 'Найти Девушку 🙋‍♀️')
@gender_required
async def process_start_search_male_command(message: Message):
    await start_search(message, desired_gender='female')


@dp.message(Command(commands=['stop']))
@gender_required
async def process_stop_dialog(message: Message):
    chat_info = await db.get_active_chat(message.chat.id)
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
        is_in_queue = await db.is_in_queue(message.chat.id)
        if is_in_queue:
            # Удаляем пользователя из очереди, если он в поиске
            await db.delete_queue(message.chat.id)
            await message.answer(
                'Поиск отменён',
                reply_markup=keyboard_before_start_search
            )
        else:
            await message.answer(
                '''Вы не в диалоге ⚠.\nНапишите /search, чтобы найти собеседника''',
                reply_markup=keyboard_before_start_search
            )


@dp.message(F.text == '❌ Завершить диалог')
@gender_required
async def process_stop_dialog(message: Message):
    chat_info = await db.get_active_chat(message.chat.id)
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


@dp.message(F.text == '✋ Остановить поиск')
@gender_required
async def process_finish_search_command(message: Message):
    # Проверяем, находится ли пользователь в очереди
    is_in_queue = await db.is_in_queue(message.chat.id)

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


@dp.message(F.text.in_(['Я Парень 🙋‍♂️', 'Я Девушка 🙋‍♀️']))
async def set_gender(message: Message):
    if message.text == 'Я Парень 🙋‍♂️':
        gender = 'male'
    elif message.text == 'Я Девушка 🙋‍♀️':
        gender = 'female'
    else:
        return  # Если сообщение не соответствует ожиданиям, ничего не делаем

    # Сохраняем пол в базу данных
    await db.set_gender(message.chat.id, gender)

    # Отправляем приветственное сообщение и клавиатуру для дальнейшего взаимодействия
    await message.answer(
        'Ваш пол успешно сохранён! Теперь вы можете начать общение.',
        reply_markup=keyboard_before_start_search
    )


@dp.message()
@gender_required
async def process_chatting(message: Message):
    chat_info = await db.get_active_chat(message.chat.id)
    if chat_info:
        await message.send_copy(chat_id=chat_info[1])
    else:
        await message.answer(
            'Вы еще не начали диалог',
            reply_markup=keyboard_before_start_search
        )


if __name__ == '__main__':
    dp.run_polling(bot)
