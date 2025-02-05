from aiogram import F, Router, Bot
from aiogram.types import Message

from app.infrastructure.database.database import Database
from app.tgbot.keyboards import *
from locales.translator import Translator
from app.tgbot.handlers.user.chat.search import start_search

router = Router()


@router.message(F.text == '👫Поиск по полу')
async def process_choose_gender_search(message: Message, translator: Translator):
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

@router.message(F.text == 'Найти Парня 🙋‍♂️')
async def process_start_search_male_command(message: Message, db: Database, bot: Bot, translator: Translator):
    await start_search(message, db, bot, translator, preferred_gender='m')


@router.message(F.text == 'Найти Девушку 🙋‍♀️')
async def process_start_search_female_command(message: Message, db: Database, bot: Bot, translator: Translator):
    await start_search(message, db, bot, translator, preferred_gender='f')


@router.message(F.text == '↩️ Назад')
async def process_cancel_choose_gender_for_search(message: Message, db: Database, bot: Bot, translator: Translator):
    await message.answer(
        translator.get('cancel_choose_search_gender'),
        reply_markup=keyboard_before_start_search
    )