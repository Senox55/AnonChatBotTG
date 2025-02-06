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
async def process_chatting(message: Message, redis: Redis, translator: Translator, bot: Bot):
    user_id = message.chat.id
    room_id = await redis.get(f"user_rooms:{user_id}")
    if not room_id:
        await message.answer(
            text=translator.get('when_not_in_dialog'),
            reply_markup=keyboard_before_start_search
        )
        return

    room_key = f"rooms:{room_id}"
    room_status = await redis.hget(f"rooms:{room_id}", "status")
    users = await redis.lrange(f"{room_key}:user_ids", 0, -1)
    room_capacity = await redis.hget(f"users:{user_id}", "preferred_room_capacity")

    if room_status == 'waiting':
        await message.answer(
            translator.get('in_search', count=len(users), capacity=room_capacity),
            reply_markup=keyboard_after_start_search
        )
        return

    logger.info(f"Сообщение в комнату: {room_id} от Пользователя: {user_id}")

    users = await redis.lrange(f"rooms:{room_id}:user_ids", 0, -1)  # Получаем всех пользователей
    capacity = await redis.hget(f"rooms:{room_id}", "capacity")
    use_nicknames = int(capacity) > 2

    for u_id in users:
        if str(user_id) == u_id:
            continue

        # try:
        safe_mode = await redis.hget(f"user_ids:{u_id}", "safe_mode")
        safe_mode_bool = safe_mode.lower() == 'true' if safe_mode else False
        logger.info(f"User {u_id} safe mode: {safe_mode}")

        if safe_mode_bool and not message.text:
            media_type = await get_media_type(message)
            await bot.send_message(
                chat_id=u_id,
                text=translator.get("hidden_content_alert", media_type=media_type)
            )
        else:
            # Если используем никнеймы, получаем их из Redis
            if use_nicknames:
                user_nickname = await redis.hget(f"rooms:{room_id}:users:{user_id}", "nickname")
                nickname = user_nickname if user_nickname else f"Пользователь"
                await bot.send_message(
                    chat_id=u_id,
                    text=f"*_{nickname}_*\n{message.text}",  # Отправляем сообщение с никнеймом
                    parse_mode='MarkdownV2'
                )
            else:
                await message.send_copy(chat_id=u_id)

    # except TelegramForbiddenError:
    #     logger.exception("TelegramForbiddenError")
    #     await message.answer(
    #         translator.get('interlocutor_blocked_bot')
    #     )
