import logging
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from redis.asyncio import Redis

from app.infrastructure.database.database import Database
from app.tgbot.keyboards import *
from config_data.user_config import SEX
from locales.translator import Translator

router = Router()

logger = logging.getLogger(__name__)


@router.message(F.text == "⚙️ Настройки поиска")
async def process_show_search_settings(message: Message, translator: Translator, redis: Redis):
    user_id = message.chat.id
    room_capacity = await redis.hget(f"users:{user_id}", key="preferred_room_capacity")
    if room_capacity == '2':
        preferred_gender = await redis.hget(f"users:{user_id}", key="preferred_gender")

        profile_message = (
            f"<b>{translator.get('search_settings_header')}</b>\n\n"
            f"{translator.get('preferred_gender', preferred_gender=SEX[preferred_gender])}\n"
            f"{translator.get('preferred_room_capacity', room_capacity=room_capacity)}\n\n"
        )
    else:
        profile_message = (
            f"<b>{translator.get('search_settings_header')}</b>\n\n"
            f"{translator.get('preferred_room_capacity', room_capacity=room_capacity)}\n\n"
        )

    await message.answer(profile_message, parse_mode="HTML", reply_markup=keyboard_change_search_settings_inline)


@router.callback_query(F.data == "search_settings_pressed")
async def process_change_search_settings(callback: CallbackQuery, translator: Translator, redis: Redis):
    logger.debug(f"User {callback.message.chat.id} start change search settings")
    await callback.message.edit_text(
        translator.get('choose_capacity_room'),
        reply_markup=keyboard_choose_room_capacity_inline
    )


@router.callback_query(F.data == "set_room_capacity_2")
async def process_set_room_capacity_2(callback: CallbackQuery, translator: Translator, db: Database, redis: Redis):
    user_id = callback.from_user.id
    await redis.hset(name=f"users:{user_id}", key="preferred_room_capacity", value="2")
    await db.update_preferred_room_capacity(user_id, 2)
    await callback.message.edit_text(
        text="Выберите желаемый пол собеседника:",
        reply_markup=keyboard_choose_preferred_gender_inline
    )


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


@router.callback_query(F.data == "choose_preferred_gender_random")
async def process_set_random_preferred_gender(callback: CallbackQuery, translator: Translator, db: Database,
                                              redis: Redis):
    user_id = callback.from_user.id
    await redis.hset(name=f"users:{user_id}", key="preferred_gender", value="r")
    await db.update_preferred_gender(user_id, "r")
    await callback.message.edit_text(translator.get('save_search_settings'),
                                     reply_markup=None)
