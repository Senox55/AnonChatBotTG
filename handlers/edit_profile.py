from aiogram import F, Router
from aiogram.types import CallbackQuery

from database.database import Database
from keyboards import *
from language.translator import Translator

router = Router()


async def set_chat_mode(callback: CallbackQuery, db: Database, translator: Translator, is_save):
    user_id = callback.from_user.id
    await db.change_user_chat_mode(user_id, is_save)
    await callback.message.edit_text(
        text=translator.get("safe_mode_enabled"),
        reply_markup=None
    )


async def set_gender(callback: CallbackQuery, db: Database, translator: Translator, gender: str):
    """
    Функция для установки пола
    :param callback:
    :param db:
    :param translator:
    :param gender:
    :return:
    """
    await db.update_gender(callback.message.chat.id, gender)
    await callback.message.edit_text(
        translator.get('set_age'),
        reply_markup=keyboard_before_change_age_inline)
    await callback.answer()


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


@router.callback_query(F.data == 'set_male_pressed')
async def process_set_male_gender(callback: CallbackQuery, db: Database, translator: Translator):
    await set_gender(callback, db, translator, 'm')


@router.callback_query(F.data == 'set_female_pressed')
async def process_set_female_gender(callback: CallbackQuery, db: Database, translator: Translator):
    await set_gender(callback, db, translator, 'f')


@router.callback_query(F.data.startswith('set_age_'))
async def process_set_age(callback: CallbackQuery, db: Database, translator: Translator):
    age_mapping = {
        'set_age_17': 17,
        'set_age_21': 21,
        'set_age_25': 25,
        'set_age_35': 35,
        'set_age_45': 45,
        'set_age_46': 46,
    }
    age = age_mapping.get(callback.data)
    if age is None:
        return

    await db.set_age(callback.message.chat.id, age)
    await callback.message.edit_text(
        text=translator.get('registered'),
        reply_markup=None
    )


@router.callback_query(F.data == 'change_chat_mode')
async def process_change_chat_mode(callback: CallbackQuery, translator: Translator):
    """
    Функция для смены режима безопасности чата
    :param callback:
    :param translator:
    :return:
    """
    await callback.message.edit_text(
        text=translator.get("choose_chat_mode"),
        reply_markup=keyboard_edit_chat_mode_inline
    )


@router.callback_query(F.data == 'safe_mode')
async def process_set_safe_chat_mode(callback: CallbackQuery, db: Database, translator: Translator):
    await set_chat_mode(callback, db, translator, 'True')


@router.callback_query(F.data == 'unsafe_mode')
async def process_set_safe_chat_mode(callback, db, translator):
    await set_chat_mode(callback, db, translator, 'False')
