from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import logging

from handlers.stop_dialog import stop_dialog
from handlers.start_search import start_search

router = Router()
logging.basicConfig(level=logging.INFO)


@router.message(Command(commands=['next']))
async def process_next_command(message: Message, db, bot, translator):
    await stop_dialog(message, db, bot, translator, from_search_next=True)

    preferred_gender = await db.get_preferred_gender(message.chat.id)

    await start_search(message, db, bot, translator, preferred_gender)
