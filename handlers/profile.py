from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from keyboards import *

router = Router()


# Определение состояний
class GenderChange(StatesGroup):
    waiting_for_gender = State()


async def show_profile(message: Message, db, translator):
    user_id = message.chat.id
    user_info = await db.get_user_info(user_id)

    if user_info:
        chat_count = user_info[3]
        gender = user_info[2]

        profile_message = (
            f"<b>Ваш профиль</b>\n\n"
            f"💬 Чатов — {chat_count}\n"
            f"Пол — {gender}\n\n"
            "Выберите, что вы хотите изменить:"
        )

        await message.answer(profile_message, parse_mode="HTML", reply_markup=keyboard_edit_profile_inline)


@router.message(Command(commands=['profile']))
async def process_show_profile_command(message: Message, db, translator):
    await show_profile(message, db, translator)


@router.message(F.text == '👤 Профиль')
async def process_show_profile_button(message: Message, db, translator):
    await show_profile(message, db, translator)


@router.callback_query(F.data == 'edit_profile_pressed')
async def process_edit_profile_press(callback: CallbackQuery, translator):
    await callback.message.edit_text(
        text=translator.get('set_gender'),
        reply_markup=keyboard_before_change_gender_inline
    )
    await callback.answer()


@router.message(F.text == 'Изменить пол')
async def change_gender(message: Message, state: FSMContext, translator):
    await message.answer(
        text=translator.get('choose_gender'),
        reply_markup=keyboard_before_change_gender_inline
    )
    await state.set_state(GenderChange.waiting_for_gender)


@router.callback_query(F.data == 'set_male_pressed')
async def process_set_male_gender(callback: CallbackQuery, db, translator):
    await db.update_gender(callback.message.chat.id, 'male')
    await callback.message.edit_text(
        translator.get('save_gender'),
        reply_markup=None)
    await callback.answer()


@router.callback_query(F.data == 'set_female_pressed')
async def process_set_female_gender(callback: CallbackQuery, db, translator):
    await db.update_gender(callback.message.chat.id, 'female')
    await callback.message.edit_text(
        translator.get('save_gender'),
        reply_markup=None)
    await callback.answer()
