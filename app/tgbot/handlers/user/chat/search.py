import logging
from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from app.tgbot.keyboards import *
from app.tgbot.utils.generate_nickname import generate_random_nickname
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

            if first_room_status == "waiting":
                key = f"rooms:{first_room_id}"

                # Добавляем текущего пользователя в комнату
                await redis.rpush(f"{key}:user_ids", user_id)

                users = await redis.lrange(f"rooms:{first_room_id}:user_ids", 0, -1)

                # Проверяем, заполнена ли комната
                if len(users) == int(room_capacity):
                    await redis.hset(f"rooms:{first_room_id}", "status", "dialog")
                    await redis.lpop("search_queue")

                else:
                    await redis.hset(f"rooms:{first_room_id}", "status", "waiting")

                # Сохраняем связь user_id -> room_id
                await redis.set(f"user_rooms:{user_id}", first_room_id)

                # Уведомляем пользователей о начале диалога, если комната заполнена
                if len(users) == int(room_capacity):
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
    user_id = message.chat.id
    room_id = await redis.get(f"user_rooms:{user_id}")
    print(room_id)
    if room_id:

        room_status = await redis.hget(f"rooms:{room_id}", "status")
        logger.info(f"Room {room_id} have status:{room_status}")

        users = await redis.lrange(f"rooms:{room_id}:user_ids", 0, -1)

        # Если комната уже в состоянии ожидания, сообщаем пользователю
        if room_status == "waiting":
            await message.answer(
                text=f"Ожидание {len(users)}/{room_capacity}",
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
        search_queue_key = f"search_queue_{room_capacity}"

        # Пытаемся взять первый чат из очереди
        first_room_id = await redis.lindex(search_queue_key, 0)
        logger.debug(f"Все комнаты в очереди: {await redis.lrange(search_queue_key, 0, -1)}")

        first_room_status = await redis.hget(f"rooms:{first_room_id}", "status")
        if first_room_status == "waiting":
            key = f"rooms:{first_room_id}"

            # Генерируем никнейм для текущего пользователя
            nickname = generate_random_nickname()

            # Добавляем текущего пользователя в комнату
            await redis.rpush(f"{key}:user_ids", user_id)

            # Сохраняем информацию о пользователе с никнеймом
            user_key = f"{key}:users:{user_id}"
            await redis.hset(user_key, mapping={
                "user_id": user_id,
                "nickname": nickname
            })

            users = await redis.lrange(f"rooms:{first_room_id}:user_ids", 0, -1)

            # Проверяем, заполнена ли комната
            if len(users) == int(room_capacity):
                await redis.hset(f"rooms:{first_room_id}", "status", "dialog")
                await redis.lpop(search_queue_key)

            else:
                await redis.hset(f"rooms:{first_room_id}", "status", "waiting")

            # Сохраняем связь user_id -> room_id
            await redis.set(f"user_rooms:{user_id}", first_room_id)

            # Уведомляем пользователей о начале диалога, если комната заполнена
            if len(users) == int(room_capacity):
                for u_id in users:
                    await bot.send_message(
                        chat_id=u_id,
                        text=translator.get('found_group', count=len(users), capacity=room_capacity),
                        reply_markup=keyboard_after_find_dialog
                    )
                return

            else:
                for u_id in users:
                    await bot.send_message(
                        chat_id=u_id,
                        text=f"Ожидание {len(users)}/{room_capacity}",
                        reply_markup=keyboard_after_start_search
                    )
                return

    room_id = await create_room(redis, room_capacity, user_id)

    search_queue_key = f"search_queue_{room_capacity}"

    # Добавляем комнату в очередь поиска
    await redis.lpush(search_queue_key, room_id)

    await message.answer(
        text=translator.get("start_search_group", count=room_capacity),
        reply_markup=keyboard_after_start_search
    )


async def start_search(message: Message, redis: Redis, bot: Bot, translator: Translator):
    user_id = message.chat.id

    room_capacity = await redis.hget(f"users:{user_id}", "preferred_room_capacity")

    if room_capacity == '2':
        await search_partner(message, redis, bot, translator, room_capacity)

    else:
        await search_group(message, redis, bot, translator, room_capacity)


@router.message(CommandStart())
async def process_start_command(message: Message, redis: Redis, bot: Bot, translator: Translator):
    await start_search(message, redis, bot, translator)


@router.message(Command(commands=['search']))
async def process_search_command(message: Message, redis: Redis, bot: Bot, translator: Translator):
    await start_search(message, redis, bot, translator)


@router.message(F.text == '🔍Начать общение')
async def process_start_search_random_command(message: Message, redis: Redis, bot: Bot, translator: Translator):
    await start_search(message, redis, bot, translator)
