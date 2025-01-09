from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher, F
from aiogram.types import Message

from keyboards import *


# Хендлер для запроса гендера
async def ask_for_gender(message: Message):
    user_id = message.chat.id

    # Проверяем, установлен ли гендер
    setted_gender = await db.get_gender(user_id)
    if setted_gender:
        await message.answer("Ваш пол уже указан. Вы можете пользоваться ботом.")
        return

    # Если гендер не установлен, запрашиваем его
    await message.answer(
        "Для начала работы укажите ваш пол:",
        reply_markup=keyboard_before_set_gender
    )


async def set_gender(message: Message):
    if not await db.get_user_info(message.chat.id):
        if message.text == 'Я Парень 🙋‍♂️':
            gender = 'male'
        elif message.text == 'Я Девушка 🙋‍♀️':
            gender = 'female'
        else:
            return  # Если сообщение не соответствует ожиданиям, ничего не делаем

        # Сохраняем пол в базу данных
        await db.set_gender(message.chat.id, gender)

        # Отправляем приветственное сообщение и клавиатуру для дальнейшего взаимодействия
        await message.answer(
            'Ваш пол успешно сохранён! Теперь вы можете начать общение.',
            reply_markup=keyboard_before_start_search
        )


def register_handlers_ask_for_gender(dp: Dispatcher):
    dp.message.register(ask_for_gender)
    dp.message.register(set_gender, F.text.in_(['Я Парень 🙋‍♂️', 'Я Девушка 🙋‍♀️']))
