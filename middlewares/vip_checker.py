import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from datetime import datetime

from keyboards import *

logger = logging.getLogger(__name__)



class VipCheckMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        db = data["db"]
        translator = data['translator']

        user_id = event.from_user.id

        vip_status = await db.get_vip_status(user_id)
        if vip_status:
            return await handler(event, data)

        if isinstance(event, CallbackQuery):
            await event.answer(translator.get('only_for_vip'))
        else:
            await event.answer(translator.get('vip_description'),
                               reply_markup=buy_vip_keyboard_inline)

class CheckValidityVipMiddleware(BaseMiddleware):
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
            logger.info(f"Дата истечения VIP: {end_date}")
            if end_date and end_date < datetime.now():
                # Если срок действия истёк, деактивируем статус
                await db.deactivate_vip_status(user_id)
                await db.set_preferred_gender(user_id, None)
                await event.answer(translator.get('deactivate_vip'),
                                   reply_markup=keyboard_before_start_search)

        return await handler(event, data)