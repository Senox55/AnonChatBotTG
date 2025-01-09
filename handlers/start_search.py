from aiogram import Dispatcher, F, Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from keyboards import *

router = Router()


async def start_search(message: Message, db, bot, desired_gender: str = 'anon'):
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
                "У вас уже есть собеседник 🤔\n/next — искать нового собеседника\n/stop — закончить диалог",
                reply_markup=keyboard_after_find_dialog
            )

    else:
        await message.answer(
            'Вы уже находитесь в поиске 🕵️‍♂️.\n'
            'Пожалуйста, немного подождите, пока мы найдем для вас собеседника. ⏳\n\n'
            'Если хотите отменить поиск, нажмите "✋ Остановить поиск" или отправьте /stop.',
            reply_markup=keyboard_after_start_research
        )


@router.message(F.text == '👫Поиск по полу')
async def process_choose_gender_search(message: Message):
    await message.answer(
        'Выберите желаемый пол собеседника:',
        reply_markup=keyboard_choose_gender_search
    )


@router.message(CommandStart())
async def process_start_command(message: Message, db, bot):
    await start_search(message, db, bot, desired_gender='anon')


@router.message(Command(commands=['search']))
async def process_search_command(message: Message, db, bot):
    await start_search(message, db, bot, desired_gender='anon')


@router.message(F.text == '🔍Начать общение')
async def process_start_search_random_command(message: Message, db, bot):
    await start_search(message, db, bot, desired_gender='anon')


@router.message(F.text == 'Найти Парня 🙋‍♂️')
async def process_start_search_male_command(message: Message, db, bot):
    await start_search(message, db, bot, desired_gender='male')


@router.message(F.text == 'Найти Девушку 🙋‍♀️')
async def process_start_search_female_command(message: Message, db, bot):
    await start_search(message, db, bot, desired_gender='female')


@router.message(F.text == '🔻 Назад')
async def process_cancel_choose_gender_for_search(message: Message):
    await message.answer(
        'Выбор отменён',
        reply_markup=keyboard_before_start_search
    )
