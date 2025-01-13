from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards import *

router = Router()


@router.callback_query(F.data == 'edit_profile_pressed')
async def process_edit_profile_press(callback: CallbackQuery, translator):
    await callback.message.edit_text(
        text=translator.get('set_gender'),
        reply_markup=keyboard_before_change_gender_inline
    )
    await callback.answer()


@router.callback_query(F.data == 'set_male_pressed')
async def process_set_male_gender(callback: CallbackQuery, db, translator):
    await db.update_gender(callback.message.chat.id, 'm')
    await callback.message.edit_text(
        translator.get('set_age'),
        reply_markup=keyboard_before_change_age_inline)
    await callback.answer()


@router.callback_query(F.data == 'set_female_pressed')
async def process_set_female_gender(callback: CallbackQuery, db, translator):
    await db.update_gender(callback.message.chat.id, 'f')
    await callback.message.edit_text(
        translator.get('set_age'),
        reply_markup=keyboard_before_change_age_inline)
    await callback.answer()


@router.callback_query(F.data.startswith('set_age_'))
async def process_set_male_gender(callback: CallbackQuery, db, translator):
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
        return  # Ignore unexpected callback data

    await db.set_age(callback.message.chat.id, age)
    await callback.message.edit_text(
        text=translator.get('registered'),
        reply_markup=None
    )
