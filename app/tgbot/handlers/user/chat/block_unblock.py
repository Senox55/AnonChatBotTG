import logging
from aiogram import Router
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.types import ChatMemberUpdated
from redis.asyncio import Redis

from app.infrastructure.database.database import Database
from app.tgbot.utils.utils import parse_user_info

router = Router()

logger = logging.getLogger(__name__)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated, db: Database, redis: Redis):
    """
    Функция для фиксации пользователей, заблокировавших бота
    :param event:
    :param db:
    :return:
    """
    user_id = event.from_user.id
    logger.info(f"User {user_id} block bot")

    await redis.delete(f"users:{user_id}")
    await db.update_alive(user_id, False)

    room_id = await redis.get(f"user_rooms:{user_id}")
    if room_id:
        key = f"rooms:{room_id}"

        # Удаляем user_id из списка пользователей комнаты
        await redis.lrem(f"{key}:users", 0, str(user_id))

        # Удаляем запись о комнатах пользователя
        await redis.delete(f"user_rooms:{user_id}")


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated, db: Database, redis:Redis):
    """
    Функция для фиксации пользователей, разблокировавших бота
    :param event:
    :param db:
    :return:
    """
    user_id = event.from_user.id
    logger.info(f"User {user_id} unblock bot")
    await db.update_alive(user_id, True)
    user_info = parse_user_info(await db.get_user_info(user_id))
    await redis.hset(name=f"users:{user_id}", mapping=user_info)
