from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command

from config_data.config import load_config
from keyboards import *

router = Router()
config = load_config('.env')


async def show_profile(message: Message, db, translator):
    user_id = message.chat.id
    user_info = await db.get_user_info(user_id)

    vip_status = await db.get_vip_status(user_id)

    if vip_status:
        vip_status_end_date = vip_status['end_date']
        vip_status_end_date = f"Активен до {vip_status_end_date.strftime('%d.%m.%Y')}"
    else:
        # Если статус не активирован
        vip_status_end_date = "Не активирован"

    if user_info:
        count_chats = user_info['count_chats']
        gender = user_info['gender']
        age = user_info['age']

        profile_message = (
            f"<b>Ваш профиль</b>\n\n"
            f"💬 Чатов — {count_chats}\n"
            f"Пол — {config.gender.genders.get(gender)}\n"
            f"Возраст - {config.age.age_ranges.get(age)}\n\n"
            f"👑 VIP статус - {vip_status_end_date}\n\n"
            "Выберите, что вы хотите изменить:"
        )

        await message.answer(profile_message, parse_mode="HTML", reply_markup=keyboard_edit_profile_inline)


@router.message(Command(commands=['profile']))
async def process_show_profile_command(message: Message, db, translator):
    await show_profile(message, db, translator)


@router.message(F.text == '👤 Профиль')
async def process_show_profile_button(message: Message, db, translator):
    await show_profile(message, db, translator)
