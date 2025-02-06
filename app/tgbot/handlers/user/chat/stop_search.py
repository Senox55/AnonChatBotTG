import logging
from aiogram import F, Router, Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import Message
from redis.asyncio import Redis

from app.tgbot.handlers.user.chat.stop_utils import dialog_exit, waiting_exit, remaining_users
from app.tgbot.keyboards import *
from locales.translator import Translator

router = Router()

logger = logging.getLogger(__name__)


@router.message(F.text == '✋ Отменить поиск')
async def process_finish_search_command(message: Message, redis: Redis, translator: Translator, bot: Bot):
    user_id = message.chat.id
    room_id = await redis.get(f"user_rooms:{user_id}")

    if not room_id:
        await message.answer(
            translator.get('stop_search_when_bot_in_search'),

            reply_markup=keyboard_before_start_search
        )
        return

    room_status = await redis.hget(f"rooms:{room_id}", "status")
    room_key = f"rooms:{room_id}"
    logger.info(f"Room status before delete: {room_status}")
    if room_status == "waiting":
        await waiting_exit(
            redis, bot, translator, user_id, room_key, message
        )

        # Удаляем пользователя из комнаты
        await redis.lrem(f"{room_key}:user_ids", 0, str(user_id))

        # Проверяем оставшихся пользователей в комнате
        await remaining_users(redis, bot, translator, room_id, room_key, room_status)

        # Удаляем запись о комнате пользователя
        await redis.delete(f"user_rooms:{user_id}")

    elif room_status == "dialog":
        await message.answer(
            translator.get('start_search_when_in_dialog'),
        )
