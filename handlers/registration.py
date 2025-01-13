from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.registration import RegistrationFSM
from keyboards import *

router = Router()


@router.message(F.text.in_(['Я Парень 🙋‍♂️', 'Я Девушка 🙋‍♀️']), StateFilter(RegistrationFSM.fill_gender))
async def set_gender(message: Message, db, translator, state: FSMContext):
    if not await db.get_user_info(message.chat.id):
        if message.text == 'Я Парень 🙋‍♂️':
            gender = 'm'
        elif message.text == 'Я Девушка 🙋‍♀️':
            gender = 'f'
        else:
            return  # Если сообщение не соответствует ожиданиям, ничего не делаем

        # Сохраняем пол в базу данных
        await db.set_gender(message.chat.id, gender)

        await message.answer(
            translator.get('set_age'),
            reply_markup=keyboard_before_set_age
        )

        await state.set_state(RegistrationFSM.fill_age)


@router.message(
    F.text.in_(['до 17 лет', 'от 18 до 21 года', 'от 22 до 25 лет', 'от 26 до 35 лет', 'от 36 до 45 лет', 'старше 46']),
    StateFilter(RegistrationFSM.fill_age))
async def set_age(message: Message, db, translator, state: FSMContext):
    if message.text == 'до 17 лет':
        age = 17
    elif message.text == 'от 18 до 21 года':
        age = 21
    elif message.text == 'от 22 до 25 лет':
        age = 25
    elif message.text == 'от 26 до 35 лет':
        age = 35
    elif message.text == 'от 36 до 45 лет':
        age = 45
    elif message.text == 'старше 46':
        age = 46
    else:
        return  # Если сообщение не соответствует ожиданиям, ничего не делаем

    # Сохраняем пол в базу данных
    await db.set_age(message.chat.id, age)

    await state.clear()

    # Отправляем приветственное сообщение и клавиатуру для дальнейшего взаимодействия
    await message.answer(
        translator.get('registered'),
        reply_markup=keyboard_before_start_search
    )
