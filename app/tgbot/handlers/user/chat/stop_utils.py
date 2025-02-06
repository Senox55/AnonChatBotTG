from aiogram.exceptions import TelegramForbiddenError
import logging

from app.infrastructure.cache.utils.room_management import delete_room
from app.tgbot.keyboards import *

logger = logging.getLogger(__name__)

async def dialog_exit(redis, bot, translator, user_id, room_key, chat_id):
    """
    Обрабатывает выход пользователя из комнаты со статусом 'dialog'.
    """
    users = await redis.lrange(f"{room_key}:user_ids", 0, -1)

    for u_id in users:
        if str(user_id) == u_id:
            await bot.send_message(
                chat_id=chat_id,
                text=translator.get("stop_dialog"),
                reply_markup=keyboard_before_start_search
            )
        else:
            try:
                await bot.send_message(
                    chat_id=u_id,
                    text=translator.get("one_interlocutor_left")
                )
            except TelegramForbiddenError:
                logger.warning(f"User {u_id} blocked the bot")


async def waiting_exit(redis, bot, translator, user_id, room_key, message):
    """
    Обрабатывает выход пользователя из комнаты со статусом 'waiting'.
    """
    users = await redis.lrange(f"{room_key}:user_ids", 0, -1)
    room_capacity = await redis.hget(f"users:{user_id}", "preferred_room_capacity")

    for u_id in users:
        if str(user_id) != u_id:
            await bot.send_message(
                chat_id=u_id,
                text=translator.get("in_search", count=len(users) - 1, capacity=room_capacity),
                reply_markup=keyboard_after_start_search
            )

    await message.answer(
        translator.get('stop_search'),
        reply_markup=keyboard_before_start_search
    )


async def remaining_users(redis, bot, translator, room_id, room_key, room_status):
    """
    Проверяет количество оставшихся пользователей в комнате и принимает соответствующие меры.
    """
    remaining_users = await redis.llen(f"{room_key}:user_ids")

    if remaining_users == 0:
        # Удаляем комнату, если нет оставшихся пользователей
        await delete_room(redis, room_id)

    elif remaining_users == 1 and room_status == "dialog":
        # Если остался один пользователь и статус "dialog", уведомляем его и закрываем комнату
        remaining_user_id = await redis.lindex(f"{room_key}:user_ids", 0)
        try:
            await bot.send_message(
                chat_id=remaining_user_id,
                text=translator.get("alone_in_room"),
                reply_markup=keyboard_before_start_search
            )
        except TelegramForbiddenError:
            logger.warning(f"User {remaining_user_id} blocked the bot")

        # Удаляем комнату
        await delete_room(redis, room_id)
