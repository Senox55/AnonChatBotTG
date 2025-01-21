from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command

from filters.is_vip_filter import IsVIP
from keyboards import *

router = Router()

@router.message(Command(commands=['vip']))
async def process_vip_command(message: Message, db, translator):
    is_vip = await IsVIP()(message, db)

    if is_vip:
        # Если есть VIP, показываем основной функционал
        await message.answer(
            translator.get('already_vip_user')
        )
    else:
        await message.answer(
            text=translator.get('vip_description'),
            reply_markup=buy_vip_keyboard_inline)