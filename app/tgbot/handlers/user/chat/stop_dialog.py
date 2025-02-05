from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramForbiddenError
from redis.asyncio import Redis
import logging
import json

from app.infrastructure.cache.utils.room_management import delete_room
from app.infrastructure.database.database import Database
from app.tgbot.keyboards import *
from locales.translator import Translator

router = Router()

logger = logging.getLogger(__name__)


async def stop_dialog(message: Message, redis: Redis, bot: Bot, translator: Translator):
    user_id = message.from_user.id

    room_id = await redis.get(f"user_rooms:{user_id}")

    if room_id:
        room_status = await redis.hget(f"rooms:{room_id}", "status")
        if room_status == "dialog":
            users = await redis.lrange(f"rooms:{room_id}:users", 0, -1)  # Получаем всех пользователей
            for u_id in users:
                if str(user_id) == u_id:
                    await bot.send_message(
                        message.chat.id,
                        translator.get('stop_dialog'),
                        reply_markup=keyboard_before_start_search,
                    )
                else:
                    try:
                        await bot.send_message(
                            chat_id=u_id,
                            text=translator.get('interlocutor_stop_dialog'),
                            reply_markup=keyboard_before_start_search
                        )
                    except TelegramForbiddenError:
                        # Если пользователь 2 заблокировал бота
                        logger.warning(f"User {u_id} block bot")

        elif room_status == "waiting":
            await message.answer(
                translator.get('stop_search'),
                reply_markup=keyboard_before_start_search
            )

        await delete_room(redis, room_id)
    else:
        await message.answer(
            translator.get('when_not_in_dialog'),
            reply_markup=keyboard_before_start_search
        )


@router.message(Command(commands=['stop']))
async def process_stop_command(message: Message, redis: Redis, bot: Bot, translator: Translator):
    await stop_dialog(message, redis, bot, translator)


@router.message(F.text == '👋 Завершить чат')
async def process_stop_button(message: Message, redis: Redis, bot: Bot, translator: Translator):
    await stop_dialog(message, redis, bot, translator)
