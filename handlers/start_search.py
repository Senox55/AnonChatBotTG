from aiogram import F, Router, Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command

from database.database import Database
from filters.is_vip_filter import IsVIP
from keyboards import *
from language.translator import Translator

router = Router()


async def start_search(message: Message, db: Database, bot: Bot, translator: Translator, preferred_gender: str = None):
    user_id = message.chat.id

    await db.set_preferred_gender(user_id, preferred_gender)

    is_in_queue = await db.is_in_queue(message.chat.id)
    chat_info = await db.get_active_chat(message.chat.id)

    chat_two = await db.get_chat(await db.get_gender(message.chat.id), preferred_gender)

    if not is_in_queue:
        if not chat_info:
            if not await db.create_chat(message.chat.id, chat_two):

                await db.add_queue(message.chat.id)
                if preferred_gender == 'm':
                    search_message = translator.get('start_search_male')
                elif preferred_gender == 'f':
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


@router.message(F.text == '👫Поиск по полу', IsVIP())
async def process_choose_gender_search(message: Message, translator: Translator, ):
    """
    Функция для выбора пола собеседника
    :param message:
    :param db:
    :param translator:
    :return:
    """

    await message.answer(
        translator.get('choose_search_gender'),
        reply_markup=keyboard_choose_gender_search
    )


@router.message(CommandStart())
async def process_start_command(message: Message, db: Database, bot: Bot, translator: Translator):
    await start_search(message, db, bot, translator)


@router.message(Command(commands=['search']))
async def process_search_command(message: Message, db: Database, bot: Bot, translator: Translator):
    await start_search(message, db, bot, translator)


@router.message(F.text == '🔍Начать общение')
async def process_start_search_random_command(message: Message, db: Database, bot: Bot, translator: Translator):
    await start_search(message, db, bot, translator)


@router.message(F.text == 'Найти Парня 🙋‍♂️', IsVIP())
async def process_start_search_male_command(message: Message, db: Database, bot: Bot, translator: Translator):
    await start_search(message, db, bot, translator, preferred_gender='m')


@router.message(F.text == 'Найти Девушку 🙋‍♀️', IsVIP())
async def process_start_search_female_command(message: Message, db: Database, bot: Bot, translator: Translator):
    await start_search(message, db, bot, translator, preferred_gender='f')


@router.message(F.text == '↩️ Назад')
async def process_cancel_choose_gender_for_search(message: Message, db: Database, bot: Bot, translator: Translator):
    await message.answer(
        translator.get('cancel_choose_search_gender'),
        reply_markup=keyboard_before_start_search
    )
