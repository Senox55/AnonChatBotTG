from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.tgbot.keyboards import *
from locales.translator import Translator

router = Router()


@router.callback_query(F.data == 'edit_profile_pressed')
async def process_edit_profile_press(callback: CallbackQuery, translator: Translator):
    """
    Функция для начала изменения профиля
    :param callback:
    :param translator:
    :return:
    """
    await callback.message.edit_text(
        text=translator.get('set_gender'),
        reply_markup=keyboard_before_change_gender_inline
    )
    await callback.answer()
