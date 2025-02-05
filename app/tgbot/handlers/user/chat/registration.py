from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.infrastructure.database.database import Database
from locales.translator import Translator
from app.tgbot.states.registration import RegistrationFSM
from app.tgbot.keyboards import *

router = Router()


@router.message(F.text.in_(['Я Парень 🙋‍♂️', 'Я Девушка 🙋‍♀️']), StateFilter(RegistrationFSM.FILL_GENDER))
async def set_gender(message: Message, db: Database, translator: Translator, state: FSMContext):
    """
    Функция для установки гендера через reply клавиатуру
    :param message:
    :param db:
    :param translator:
    :param state:
    :return:
    """
    if not await db.get_user_info(message.chat.id):
        if message.text == 'Я Парень 🙋‍♂️':
            gender = 'm'
        elif message.text == 'Я Девушка 🙋‍♀️':
            gender = 'f'
        else:
            return  # Если сообщение не соответствует ожиданиям, ничего не делаем

        await state.update_data(gender=gender)

        await message.answer(
            translator.get('set_age'),
            reply_markup=keyboard_before_set_age
        )

        await state.set_state(RegistrationFSM.FILL_AGE)


@router.message(
    F.text.in_(['📍 До 17', '📍 18-21', '📍 22-25', '📍 26-35', '📍 36-45', '📍 46+']),
    StateFilter(RegistrationFSM.FILL_AGE))
async def set_age(message: Message, db: Database, translator: Translator, state: FSMContext):
    """
    Функция для установки пола через reply клавиатуру
    :param message:
    :param db:
    :param translator:
    :param state:
    :return:
    """
    if message.text == '📍 До 17':
        age = 17
    elif message.text == '📍 18-21':
        age = 21
    elif message.text == '📍 22-25':
        age = 25
    elif message.text == '📍 26-35':
        age = 35
    elif message.text == '📍 36-45':
        age = 45
    elif message.text == '📍 46+':
        age = 46
    else:
        return  # Если сообщение не соответствует ожиданиям, ничего не делаем

    user_data = await state.get_data()
    gender = user_data.get('gender')

    # Сохраняем данные в базу данных
    await db.add_user(message.chat.id, gender, age)

    await state.clear()

    # Отправляем приветственное сообщение и клавиатуру для дальнейшего взаимодействия
    await message.answer(
        translator.get('registered'),
        reply_markup=keyboard_before_start_search
    )
