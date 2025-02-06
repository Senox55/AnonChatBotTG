import logging
from redis.asyncio import Redis
from datetime import datetime

from app.tgbot.utils.generate_nickname import generate_random_nickname

logger = logging.getLogger(__name__)

async def create_room(redis: Redis, capacity: int, user_id: int, status: str = "waiting"):
    room_id = await redis.incr("room_counter")

    key = f"rooms:{room_id}"

    nickname = generate_random_nickname()

    await redis.hset(key, mapping={
        "room_number": room_id,
        "capacity": capacity,
        "status": status,
        "created": datetime.now().timestamp()
    })

    user_key = f"{key}:users:{user_id}"
    await redis.hset(user_key, mapping={
        "user_id": user_id,
        "nickname": nickname
    })

    # Добавляем пользователя в список идентификаторов пользователей комнаты
    await redis.rpush(f"{key}:user_ids", user_id)

    logger.info(f"В Комнату {room_id} добавлен Пользователь: {user_id} с Никнеймом {nickname}.")

    await redis.set(f"user_rooms:{user_id}", room_id)
    return room_id

async def delete_room(redis: Redis, room_id: int):
    key = f"rooms:{room_id}"
    users = await redis.lrange(f"rooms:{room_id}:user_ids", 0, -1)
    for user_id in users:
        await redis.delete(f"{key}:users:{user_id}")
        await redis.delete(f"user_rooms:{user_id}")

    # Удаляем сам список пользователей
    await redis.delete(f"{key}:user_ids")

    # Удаляем ключ комнаты
    await redis.delete(key)