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


async def show_profile(message: Message, db):
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
async def process_show_profile_command(message: Message, db):
    await show_profile(message, db)


@router.message(F.text == '👤 Профиль')
async def process_show_profile_button(message: Message, db):
    await show_profile(message, db)


@router.callback_query(F.data == 'edit_profile_pressed')
async def process_edit_profile_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text='1.Укажите ваш пол:',
        reply_markup=keyboard_before_change_gender_inline
    )
    await callback.answer()


@router.message(F.text == 'Изменить пол')
async def change_gender(message: Message, state: FSMContext):
    await message.answer(
        "Выберите ваш пол:\n"
        "Мужчина \n"
        "Женщина",
        reply_markup=keyboard_before_change_gender_inline
    )
    await state.set_state(GenderChange.waiting_for_gender)


async def set_gender_for_profile(message: Message, state: FSMContext, db):
    if message.text == 'Мужчина':
        gender = 'male'
    elif message.text == 'Женщина':
        gender = 'female'
    else:
        return  # Если сообщение не соответствует ожиданиям, ничего не делаем

    # Обновляем пол в базе данных
    await db.update_gender(message.chat.id, gender)

    # Отправляем подтверждение и возвращаемся к редактированию профиля
    await message.answer(
        'Ваш пол успешно изменён!',
        reply_markup=keyboard_before_start_search
    )
    await state.clear()


@router.callback_query(F.data == 'set_male_pressed')
async def process_set_male_gender(callback: CallbackQuery, db):
    await db.update_gender(callback.message.chat.id, 'male')
    await callback.message.edit_text(
        'Ваш пол успешно сохранён! Теперь вы можете начать общение.',
        reply_markup=None)
    await callback.answer()


@router.callback_query(F.data == 'set_female_pressed')
async def process_set_female_gender(callback: CallbackQuery, db):
    await db.update_gender(callback.message.chat.id, 'female')
    await callback.message.edit_text(
        'Ваш пол успешно сохранён! Теперь вы можете начать общение.',
        reply_markup=None)
    await callback.answer()
