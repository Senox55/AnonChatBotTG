import logging
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from redis.asyncio import Redis

from config_data.config import load_config
from app.infrastructure.database.database import Database
from app.tgbot.keyboards import *
from locales.translator import Translator

router = Router()
config = load_config('.env')

logger = logging.getLogger(__name__)


async def set_chat_mode(callback: CallbackQuery, db: Database, redis: Redis, translator: Translator, is_save):
    user_id = callback.from_user.id
    await redis.hset(name=f"users:{user_id}", key="safe_mode", value=str(is_save))
    await db.update_chat_mode(user_id, is_save)
    if is_save:
        await callback.message.edit_text(
            text=translator.get("safe_mode_enabled"),
            reply_markup=None
        )
    else:
        await callback.message.edit_text(
            text=translator.get("safe_mode_disabled"),
            reply_markup=None
        )


async def update_gender(callback: CallbackQuery, db: Database, redis: Redis, translator: Translator, gender: str):
    """
    Функция для изменения пола
    Args:
        callback:
        db:
        redis:
        translator:
        gender:

    Returns:

    """
    user_id = callback.message.chat.id
    await db.update_gender(user_id, gender)
    await redis.hset(name=f"users:{user_id}", key="gender", value=gender)
    await callback.message.edit_text(
        translator.get('set_age'),
        reply_markup=keyboard_before_change_age_inline)
    await callback.answer()



@router.callback_query(F.data == 'set_male_pressed')
async def process_set_male_gender(callback: CallbackQuery, db: Database, redis: Redis, translator: Translator):
    await update_gender(callback, db, redis, translator, 'm')


@router.callback_query(F.data == 'set_female_pressed')
async def process_set_female_gender(callback: CallbackQuery, db: Database, redis: Redis, translator: Translator):
    await update_gender(callback, db, redis, translator, 'f')


@router.callback_query(F.data.startswith('set_age_'))
async def process_update_age(callback: CallbackQuery, db: Database, redis: Redis, translator: Translator):
    user_id = callback.message.chat.id
    age_mapping = {
        'set_age_17': 17,
        'set_age_21': 21,
        'set_age_25': 25,
        'set_age_35': 35,
        'set_age_45': 45,
        'set_age_46': 46,
    }
    age = age_mapping.get(callback.data)
    if age is None:
        return

    await db.update_age(user_id, age)
    await redis.hset(name=f"users:{user_id}", key="age", value=str(age))

    await callback.message.edit_text(
        text=translator.get('registered'),
        reply_markup=None
    )


@router.callback_query(F.data == 'change_chat_mode')
async def process_change_chat_mode(callback: CallbackQuery, translator: Translator):
    """
    Функция для смены режима безопасности чата
    :param callback:
    :param translator:
    :return:
    """
    await callback.message.edit_text(
        text=translator.get("choose_chat_mode"),
        reply_markup=keyboard_edit_chat_mode_inline
    )


@router.callback_query(F.data == 'safe_mode')
async def process_set_safe_chat_mode(callback: CallbackQuery, db: Database, redis: Redis, translator: Translator):
    await set_chat_mode(callback, db, redis,translator, True)


@router.callback_query(F.data == 'unsafe_mode')
async def process_set_safe_chat_mode(callback: CallbackQuery, db: Database, redis: Redis, translator: Translator):
    await set_chat_mode(callback, db, redis, translator, False)


@router.message(Command(commands=['settings']))
async def process_change_settings(message: Message, translator: Translator):
    logger.debug(f"User {message.chat.id} start change settings")
    await message.answer(
        translator.get('change_settings'),
        reply_markup=keyboard_edit_settings_inline
    )
