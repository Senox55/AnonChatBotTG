from aiogram import Router, Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import Message
import logging

from database.database import Database
from language.translator import Translator
from handlers.user.chat_utils import close_game_after_stop_dialog
from keyboards import *


router = Router()


@router.message()
async def process_chatting(message: Message, db: Database, translator: Translator, bot: Bot):
    user_id_one = message.chat.id
    chat_info = await db.get_active_chat(user_id_one)
    is_in_queue = await db.is_in_queue(user_id_one)

    if chat_info:
        user_id_two = chat_info[1]
        try:
            # Получаем режим собеседника
            receiver_safe_mode = await db.get_user_chat_mode(user_id_two)

            logging.info(f"Пользователь {user_id_two} имеет safe mode = {receiver_safe_mode}")

            if message.photo and receiver_safe_mode:
                photo = message.photo[-1]
                # Отправляем фото как спойлер
                await bot.send_photo(
                    chat_id=user_id_two,
                    photo=photo.file_id,
                    caption=message.caption,
                    has_spoiler=True
                )


            elif message.video and receiver_safe_mode:
                # Отправляем видео как спойлер
                await bot.send_video(
                    chat_id=user_id_two,
                    video=message.video.file_id,
                    caption=message.caption,
                    has_spoiler=True

                )

            elif message.animation and receiver_safe_mode:
                # Отправляем GIF как спойлер
                await bot.send_animation(
                    chat_id=user_id_two,
                    animation=message.animation.file_id,
                    caption=message.caption,
                    has_spoiler=True
                )
            else:
                # Для всех остальных сообщений или когда безопасный режим выключен
                await message.send_copy(chat_id=user_id_two)

        except TelegramForbiddenError:
            logging.info(TelegramForbiddenError)
            await close_game_after_stop_dialog(message, db, translator, bot)
            await message.answer(translator.get('interlocutor_blocked_bot'), reply_markup=keyboard_before_start_search)

    elif is_in_queue:
        await message.answer(
            translator.get('start_search_when_in_search'),
            reply_markup=keyboard_after_start_research
        )
    else:
        await message.answer(
            translator.get('when_not_in_dialog'),
            reply_markup=keyboard_before_start_search
        )
