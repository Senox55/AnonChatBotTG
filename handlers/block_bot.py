import logging

from aiogram import Router
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.types import ChatMemberUpdated

router = Router()

logging.basicConfig(level=logging.INFO)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated, db):
    user_id = event.from_user.id
    logging.info(f"Пользователь {user_id} заблокировал бота")

    await db.set_alive_to_false(user_id)

    if await db.is_in_queue(user_id):
        await db.delete_queue(user_id)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated, db):
    user_id = event.from_user.id
    logging.info(f"Пользователь {user_id} разблокировал бота")
    await db.set_alive_to_true(user_id)
