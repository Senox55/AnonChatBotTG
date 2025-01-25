from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
import logging

from database.database import Database
from handlers.user.stop_dialog import stop_dialog
from handlers.user.search import start_search
from language.translator import Translator

router = Router()
logging.basicConfig(level=logging.INFO)


@router.message(Command(commands=['next']))
async def process_next_command(message: Message, db: Database, bot: Bot, translator: Translator):
    """
    Функция для завершения диалога и поиска следующего собеседника
    :param message:
    :param db:
    :param bot:
    :param translator:
    :return:
    """
    await stop_dialog(message, db, bot, translator, from_search_next=True)

    preferred_gender = await db.get_preferred_gender(message.chat.id)

    await start_search(message, db, bot, translator, preferred_gender)
