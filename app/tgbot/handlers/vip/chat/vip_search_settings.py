import logging
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from redis.asyncio import Redis

from app.infrastructure.database.database import Database
from app.tgbot.keyboards import *
from locales.translator import Translator

router = Router()

logger = logging.getLogger(__name__)

@router.callback_query(F.data == "choose_preferred_gender_male")
async def process_set_random_preferred_gender(callback: CallbackQuery, translator: Translator, db: Database, redis: Redis):
    user_id = callback.from_user.id
    await redis.hset(name=f"users:{user_id}", key="preferred_gender", value="m")
    await db.update_preferred_gender(user_id,  "m")
    await callback.message.edit_text(translator.get('save_search_settings'),
                                     reply_markup=None)


@router.callback_query(F.data == "choose_preferred_gender_female")
async def process_set_random_preferred_gender(callback: CallbackQuery, translator: Translator, db: Database, redis: Redis):
    user_id = callback.from_user.id
    await redis.hset(name=f"users:{user_id}", key="preferred_gender", value="f")
    await db.update_preferred_gender(user_id,  "f")
    await callback.message.edit_text(translator.get('save_search_settings'),
                                     reply_markup=None)