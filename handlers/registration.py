from aiogram import F, Router
from aiogram.types import Message

from keyboards import *

router = Router()


@router.message(F.text.in_(['Я Парень 🙋‍♂️', 'Я Девушка 🙋‍♀️']))
async def set_gender(message: Message, db):
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
