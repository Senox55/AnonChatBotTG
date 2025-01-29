import logging
from aiogram import Router, Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import Message

from database.database import Database
from language.translator import Translator
from handlers.user.chat.chat_utils import close_game_after_stop_dialog
from keyboards import *

router = Router()

logger = logging.getLogger(__name__)


async def get_media_type(message):
    media_types = {
        'photo': 'фото',
        'video': 'видео',
        'animation': 'GIF',
        'sticker': 'стикер',
        'voice': 'голосовое',
        'document': 'файл'
    }

    for attr, type_name in media_types.items():
        if getattr(message, attr):
            return type_name
    return 'файл'


@router.message()
async def process_chatting(message: Message, db: Database, translator: Translator, bot: Bot):
    user_id = message.chat.id
    chat_info = await db.get_active_chat(user_id)
    is_in_queue = await db.is_in_queue(user_id)

    if not chat_info and not is_in_queue:
        await message.answer(
            translator.get('not_in_chat'),
            reply_markup=keyboard_before_start_search
        )
        return

    if is_in_queue:
        await message.answer(
            translator.get('in_queue'),
            reply_markup=keyboard_after_start_research
        )
        return

    partner_id = chat_info[1]
    try:
        safe_mode = await db.get_user_chat_mode(partner_id)
        logger.info(f"User {partner_id} safe mode: {safe_mode}")

        if safe_mode and not message.text:
            media_type = await get_media_type(message)
            await bot.send_message(
                chat_id=partner_id,
                text=translator.get("hidden_content_alert", media_type=media_type)
            )
        else:
            await message.send_copy(chat_id=partner_id)

    except TelegramForbiddenError:
        logger.exception("TelegramForbiddenError")
        await close_game_after_stop_dialog(message, db, translator, bot)
        await message.answer(
            translator.get('chat_ended'),
            reply_markup=keyboard_edit_settings_inline
        )
