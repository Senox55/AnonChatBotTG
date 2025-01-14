from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

from states.registration import RegistrationFSM
from keyboards import *


class RegistrationCheckMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        """
        Любое входящее сообщение проверяем:
        - Есть ли пол и возраст в базе?
        - Если нет, ставим пользователю FSM.fill_gender или fill_age
          (смотря, что отсутствует) и просим ввести.
        - И не даём идти дальше по хендлерам.
        """
        db = data["db"]
        translator = data['translator']
        state = data["state"]  # FSMContext из data

        user_id = event.chat.id

        gender = await db.get_gender(user_id)
        age = await db.get_age(user_id)
        if not gender:
            # Показываем сообщение про "выберите пол"
            await state.set_state(RegistrationFSM.fill_gender)
            if event.text in (
                    ["Я Парень 🙋‍♂️", "Я Девушка 🙋‍♀️"]):
                return await handler(event, data)
            await event.answer(translator.get('set_gender'),
                               reply_markup=keyboard_before_set_gender)
            return  # Прерываем, чтобы не вызывать основной handler
        elif not age:
            await state.set_state(RegistrationFSM.fill_age)
            if event.text in (
                    ['📍 До 17', '📍 18-21', '📍 22-25', '📍 26-35', '📍 36-45', '📍 46+']):
                return await handler(event, data)
            await event.answer(translator.get('set_age'),
                               reply_markup=keyboard_before_set_age)
            return

        # Если всё нормально (либо зарегистрирован, либо уже внутри FSM), идём дальше.
        return await handler(event, data)
