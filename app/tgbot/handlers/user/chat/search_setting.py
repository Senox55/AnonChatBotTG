import logging
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from redis.asyncio import Redis

from app.infrastructure.database.database import Database
from app.tgbot.keyboards import *
from locales.translator import Translator

router = Router()

logger = logging.getLogger(__name__)


@router.message(F.text == "⚙️ Настройки поиска")
async def process_change_search_settings(message: Message, translator: Translator):
    logger.debug(f"User {message.chat.id} start change search settings")
    await message.answer(
        translator.get('choose_capacity_room'),
        reply_markup=keyboard_choose_room_capacity
    )


@router.callback_query(F.data == "set_room_capacity_2")
async def process_set_room_capacity_2(callback: CallbackQuery, translator: Translator, db: Database, redis: Redis):
    user_id = callback.from_user.id
    await redis.hset(name=f"users:{user_id}", key="preferred_room_capacity", value="2")
    await db.update_preferred_room_capacity(user_id, 2)
    await callback.message.edit_text(translator.get('save_search_settings'),
                                                    reply_markup=None)


@router.callback_query(F.data == "set_room_capacity_3")
async def process_set_room_capacity_3(callback: CallbackQuery, translator: Translator, db: Database, redis: Redis):
    user_id = callback.from_user.id
    await redis.hset(name=f"users:{user_id}", key="preferred_room_capacity", value="3")
    await db.update_preferred_room_capacity(user_id, 2)
    await callback.message.edit_text(translator.get('save_search_settings'),
                                                    reply_markup=None)


@router.callback_query(F.data == "set_room_capacity_4")
async def process_set_room_capacity_4(callback: CallbackQuery, translator: Translator, db: Database, redis: Redis):
    user_id = callback.from_user.id
    await redis.hset(name=f"users:{user_id}", key="preferred_room_capacity", value="4")
    await db.update_preferred_room_capacity(user_id, 2)
    await callback.message.edit_text(translator.get('save_search_settings'),
                                                    reply_markup=None)
