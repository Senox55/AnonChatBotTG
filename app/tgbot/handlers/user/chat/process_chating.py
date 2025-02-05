import logging
from aiogram import Router, Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import Message
from redis.asyncio import Redis

from app.infrastructure.database.database import Database
from app.tgbot.keyboards import *
from locales.translator import Translator

router = Router()

logger = logging.getLogger(__name__)


async def get_media_type(message):
    media_types = {
        'photo': 'фото',
        'video': 'видео',
        'animation': 'GIF',
        'sticker': 'стикер',
        'voice': 'голосовое',
        'document': 'файл'
    }

    for attr, type_name in media_types.items():
        if getattr(message, attr):
            return type_name
    return 'файл'


@router.message()
async def process_chatting(message: Message, db: Database, redis: Redis, translator: Translator, bot: Bot):
    user_id = message.chat.id
    room_id = await redis.get(f"user_rooms:{user_id}")
    if not room_id:
        await message.answer(
                    text=translator.get('when_not_in_dialog'),
                    reply_markup=keyboard_before_start_search
                )
        return

    room_status = await redis.hget(f"rooms:{room_id}", "status")

    if room_status == "waiting":
        await message.answer(
            text=translator.get('in_search'),
            reply_markup=keyboard_after_start_search
        )
        return

    users = await redis.lrange(f"rooms:{room_id}:users", 0, -1)  # Получаем всех пользователей

    for u_id in users:
        if str(user_id) == u_id:
            continue
        try:
            safe_mode = await redis.hget(f"users:{u_id}", "safe_mode")

            safe_mode_bool = safe_mode.lower() == 'true' if safe_mode else False
            logger.info(f"User {u_id} safe mode: {safe_mode}")

            if safe_mode_bool and not message.text:
                media_type = await get_media_type(message)
                await bot.send_message(
                    chat_id=u_id,
                    text=translator.get("hidden_content_alert", media_type=media_type)
                )
            else:
                await message.send_copy(chat_id=u_id)

        except TelegramForbiddenError:
            logger.exception("TelegramForbiddenError")
            await message.answer(
                translator.get('interlocutor_blocked_bot')
            )
    return
