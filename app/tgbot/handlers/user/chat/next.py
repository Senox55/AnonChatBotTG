import logging
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from redis.asyncio import Redis

from app.tgbot.handlers.user.chat.stop_dialog import stop_dialog
from app.tgbot.handlers.user.chat.search import start_search
from app.tgbot.keyboards import keyboard_before_start_search, keyboard_after_start_search
from locales.translator import Translator

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command(commands=['next']))
async def process_next_command(message: Message, redis: Redis, bot: Bot, translator: Translator):
    """
    Функция для завершения диалога и поиска следующего собеседника
    :param message:
    :param redis:
    :param bot:
    :param translator:
    :return:
    """
    user_id = message.chat.id
    room_id = await redis.get(f"user_rooms:{user_id}")
    if room_id:
        room_key = f"rooms:{room_id}"
        room_status = await redis.hget(f"rooms:{room_id}", "status")
        users = await redis.lrange(f"{room_key}:user_ids", 0, -1)
        room_capacity = await redis.hget(f"users:{user_id}", "preferred_room_capacity")
        if room_status == 'waiting':
            await message.answer(
                translator.get('in_search', count=len(users), capacity=room_capacity),
                reply_markup=keyboard_after_start_search
            )
        elif room_status == 'dialog':
            await stop_dialog(message, redis, bot, translator)
            await start_search(message, redis, bot, translator)
    else:
        await start_search(message, redis, bot, translator)
