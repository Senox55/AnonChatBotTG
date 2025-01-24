from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command

from database.database import Database
from filters.is_vip_filter import IsVIP
from keyboards import *
from language.translator import Translator

router = Router()


@router.message(Command(commands=['vip']), IsVIP())
async def process_vip_command(message: Message, translator: Translator):
    await message.answer(
        translator.get('already_vip_user')
    )
