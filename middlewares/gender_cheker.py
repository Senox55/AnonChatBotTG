from typing import Callable, Dict, Any, Awaitable, Union
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from keyboards import *


class GenderCheckerMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        if event.message:
            user_id = event.message.from_user.id
            event_obj = event.message
        elif event.callback_query:
            user_id = event.callback_query.from_user.id
            event_obj = event.callback_query
        else:
            # Если это другой тип обновления, пропускаем проверку
            return await handler(event, data)

        db = data["db"]

        # Проверяем команды, которые должны быть доступны без установки гендера
        if isinstance(event_obj, Message) and event_obj.text and event_obj.text in (
        ['Я Парень 🙋‍♂️', 'Я Девушка 🙋‍♀️']):
            return await handler(event, data)

        # Проверяем наличие гендера
        gender = await db.get_gender(user_id)
        if not gender:
            if isinstance(event_obj, Message):
                await event_obj.answer(
                    "Для начала работы укажите ваш пол:",
                    reply_markup=keyboard_before_set_gender
                )
            elif isinstance(event_obj, CallbackQuery):
                await event_obj.answer("Сначала укажите ваш пол", show_alert=True)
            return

        return await handler(event, data)
