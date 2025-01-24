from aiogram import Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message
import logging
import json

from handlers.stop_dialog import increment_chat_count
from keyboards import *

router = Router()


@router.message()
async def process_chatting(message: Message, db, translator, bot):
    user_id_one = message.chat.id
    chat_info = await db.get_active_chat(message.chat.id)
    user_id_two = chat_info[1]
    is_in_queue = await db.is_in_queue(message.chat.id)

    if chat_info:
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
            await increment_chat_count(message.chat.id, db)
            await increment_chat_count(user_id_two, db)

            user_state_one = await db.get_user_state(user_id_one)

            if user_state_one:
                user_data_one = json.loads(user_state_one['data'])

                user_one_message_id = user_data_one.get('message_id')

                await bot.edit_message_text(
                    chat_id=user_id_one,
                    message_id=user_one_message_id,
                    text="Игра завершена. Вы покинули чат."
                )
            await db.clear_user_state(user_id_one)
            await db.delete_chat(chat_info[0])
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
