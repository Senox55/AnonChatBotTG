from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from datetime import datetime
import logging

from keyboards import keyboard_before_start_search


class VipCheckMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        db = data["db"]
        translator = data['translator']

        user_id = event.chat.id

        vip_status = await db.get_vip_status(user_id)
        if vip_status:
            end_date = vip_status['end_date']
            logging.info(f"Дата истечения VIP: {end_date}")
            if end_date and end_date < datetime.now():
                # Если срок действия истёк, деактивируем статус
                await db.deactivate_vip_status(user_id)
                await db.set_preferred_gender(user_id, None)
                await event.answer(translator.get('deactivate_vip'),
                                   reply_markup=keyboard_before_start_search)

        return await handler(event, data)
