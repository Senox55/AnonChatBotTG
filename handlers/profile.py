from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command

from config_data.config import load_config
from config_data.user_config import AGE, SEX
from database.database import Database
from keyboards import *
from language.translator import Translator

router = Router()
config = load_config('.env')


async def show_profile(message: Message, db: Database, translator: Translator):
    """
    Функция для отображения профиля пользователя
    :param message:
    :param db:
    :param translator:
    :return:
    """
    user_id = message.chat.id
    user_info = await db.get_user_info(user_id)

    vip_status = await db.get_vip_status(user_id)

    if vip_status:
        vip_status_end_date = vip_status['end_date'].strftime('%d.%m.%Y %H:%M:%S')
        vip_status_message = translator.get(
            "vip-status-active", date=vip_status_end_date
        )
    else:
        vip_status_message = translator.get("vip-status-inactive")

    if user_info:
        count_chats = user_info['count_chats']
        gender = user_info['gender']
        age = user_info['age']

        profile_message = (
            f"<b>{translator.get('profile-header')}</b>\n\n"
            f"{translator.get('chat-count', count=count_chats)}\n"
            f"{translator.get('gender', gender=SEX[gender])}\n"
            f"{translator.get('age', age=AGE[age])}\n\n"
            f"{translator.get('vip-status', vip_status=vip_status_message)}\n\n"
            f"{translator.get('profile-footer')}"
        )

        await message.answer(profile_message, parse_mode="HTML", reply_markup=keyboard_edit_profile_inline)


@router.message(Command(commands=['profile']))
async def process_show_profile_command(message: Message, db: Database, translator: Translator):
    await show_profile(message, db, translator)


@router.message(F.text == '👤 Профиль')
async def process_show_profile_button(message: Message, db: Database, translator: Translator):
    await show_profile(message, db, translator)
