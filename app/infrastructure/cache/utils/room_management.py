import logging
from redis.asyncio import Redis
from datetime import datetime

logger = logging.getLogger(__name__)

async def create_room(redis: Redis, capacity: int, user_id: int, status: str = "waiting"):
    room_id = await redis.incr("room_counter")

    key = f"rooms:{room_id}"

    await redis.hset(key, mapping={
        "room_number": room_id,
        "capacity": capacity,
        "status": status,
        "created": datetime.now().timestamp()
    })

    await redis.rpush(f"{key}:users", user_id)

    logger.info(f"Комната {room_id} добавлена.")

    await redis.set(f"user_rooms:{user_id}", room_id)
    return room_id

async def delete_room(redis: Redis, room_id: int):
    key = f"rooms:{room_id}"
    users = await redis.lrange(f"rooms:{room_id}:users", 0, -1)
    for user_id in users:
        await redis.delete(f"{key}:users:{user_id}")
        await redis.delete(f"user_rooms:{user_id}")
    await redis.delete(key)