import logging
from aiogram import F, Router
from aiogram.types import Message
from redis.asyncio import Redis

from app.infrastructure.cache.utils.room_management import delete_room
from app.tgbot.keyboards import *
from locales.translator import Translator

router = Router()

logger = logging.getLogger(__name__)


@router.message(F.text == '✋ Отменить поиск')
async def process_finish_search_command(message: Message, redis: Redis, translator: Translator):
    user_id = message.chat.id
    room_id = await redis.get(f"user_rooms:{user_id}")

    if room_id:
        room_status = await redis.hget(f"rooms:{room_id}", "status")
        logger.info(f"Room status before delete: {room_status}")
        if room_status == "waiting":
            await message.answer(
                translator.get('stop_search'),
                reply_markup=keyboard_before_start_search
            )
            await delete_room(redis, room_id)

    else:
        await message.answer(
            translator.get('stop_search_when_bot_in_search'),

            reply_markup=keyboard_before_start_search
        )
