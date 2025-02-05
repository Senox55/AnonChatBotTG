import logging
import aiogram
from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from app.tgbot.keyboards import *
from locales.translator import Translator
from app.infrastructure.cache.utils.room_management import create_room
from redis.asyncio import Redis

router = Router()

logger = logging.getLogger(__name__)


async def search_partner(message: Message, redis: Redis, bot: Bot, translator: Translator, room_capacity):
    user_id = message.chat.id
    room_id = await redis.get(f"user_rooms:{user_id}")
    if room_id:
        room_status = await redis.hget(f"rooms:{room_id}", "status")
        logger.info(f"Room {room_id} have status:{room_status}")

        # Если комната уже в состоянии ожидания, сообщаем пользователю
        if room_status == "waiting":
            await message.answer(
                translator.get('in_search'),
                reply_markup=keyboard_after_start_search
            )
            return
        elif room_status == "dialog":
            await message.answer(
                translator.get('start_search_when_in_dialog'),
                reply_markup=keyboard_after_start_search
            )
            return

    else:

        # Пытаемся взять первый чат из очереди
        first_room_id = await redis.lindex("search_queue", 0)
        if first_room_id:

            # Проверяем статус комнаты
            first_room_status = await redis.hget(f"rooms:{first_room_id}", "status")
            capacity = await redis.hget(f"rooms:{first_room_id}", "capacity")
            if first_room_status == "waiting":
                key = f"rooms:{first_room_id}"

                # Добавляем текущего пользователя в комнату
                await redis.rpush(f"{key}:users", user_id)

                users = await redis.lrange(f"rooms:{first_room_id}:users", 0, -1)

                # Проверяем, заполнена ли комната
                if len(users) == int(capacity):
                    await redis.hset(f"rooms:{first_room_id}", "status", "dialog")
                    await redis.lpop("search_queue")
                else:
                    await redis.hset(f"rooms:{first_room_id}", "status", "waiting")

                # Сохраняем связь user_id -> room_id
                await redis.set(f"user_rooms:{user_id}", first_room_id)

                # Уведомляем пользователей о начале диалога, если комната заполнена
                if len(users) == int(capacity):
                    for u_id in users:
                        await bot.send_message(
                            chat_id=u_id,
                            text=translator.get('found_interlocutor'),
                            reply_markup=keyboard_after_find_dialog
                        )
                    return
                return
        room_id = await create_room(redis, room_capacity, user_id)

        # Добавляем комнату в очередь поиска
        await redis.lpush("search_queue", room_id)

        search_message = translator.get('start_search')
        await message.answer(
            search_message,
            reply_markup=keyboard_after_start_search
        )


async def search_group(message: Message, redis: Redis, bot: Bot, translator: Translator, room_capacity):
    pass



async def start_search(message: Message, redis: Redis, bot: Bot, translator: Translator):
    user_id = message.chat.id

    user_info = await redis.hgetall(f"users:{user_id}")

    room_capacity = user_info.get("preferred_room_capacity")

    if room_capacity == '2':
        await search_partner(message, redis, bot, translator, room_capacity)

    else:
        await message.answer("Поиск группы находится в стадии разработки")



@router.message(CommandStart())
async def process_start_command(message: Message, redis: Redis, bot: Bot, translator: Translator):
    await start_search(message, redis, bot, translator)


@router.message(Command(commands=['search']))
async def process_search_command(message: Message, redis: Redis, bot: Bot, translator: Translator):
    await start_search(message, redis, bot, translator)


@router.message(F.text == '🔍Начать общение')
async def process_start_search_random_command(message: Message, redis: Redis, bot: Bot, translator: Translator):
    await start_search(message, redis, bot, translator)
