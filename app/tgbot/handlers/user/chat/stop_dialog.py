from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from redis.asyncio import Redis
import logging

from app.tgbot.handlers.user.chat.stop_utils import dialog_exit, waiting_exit, remaining_users
from app.tgbot.keyboards import *
from locales.translator import Translator

router = Router()

logger = logging.getLogger(__name__)


async def stop_dialog(message: Message, redis: Redis, bot: Bot, translator: Translator):
    user_id = message.from_user.id
    room_id = await redis.get(f"user_rooms:{user_id}")

    if not room_id:
        # Пользователь не находится в комнате
        await message.answer(
            translator.get('when_not_in_dialog'),
            reply_markup=keyboard_before_start_search
        )
        return

    # Получаем статус комнаты и ключ
    room_status = await redis.hget(f"rooms:{room_id}", "status")
    room_key = f"rooms:{room_id}"

    # Обрабатываем разные статусы комнаты
    if room_status == "dialog":
        await dialog_exit(
            redis, bot, translator, user_id, room_key, message.chat.id
        )
    elif room_status == "waiting":
        await waiting_exit(
            redis, bot, translator, user_id, room_key, message
        )

    # Удаляем пользователя из комнаты
    await redis.lrem(f"{room_key}:user_ids", 0, str(user_id))

    # Проверяем оставшихся пользователей в комнате
    await remaining_users(redis, bot, translator, room_id, room_key, room_status)

    # Удаляем запись о комнате пользователя
    await redis.delete(f"user_rooms:{user_id}")


@router.message(Command(commands=['stop']))
async def process_stop_command(message: Message, redis: Redis, bot: Bot, translator: Translator):
    await stop_dialog(message, redis, bot, translator)


@router.message(F.text == '👋 Завершить чат')
async def process_stop_button(message: Message, redis: Redis, bot: Bot, translator: Translator):
    await stop_dialog(message, redis, bot, translator)
