import logging

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import CallbackQuery
import json

from filters.is_in_chat_filter import IsINChat
from filters.db_state_filter import DBStateFilter
from games.game_xo import GameBoard
from keyboards import *

router = Router()


@router.callback_query(F.data == "invite_play_xo", IsINChat())
async def process_choose_xo_game_mode(callback: CallbackQuery, db, translator):
    await callback.message.edit_text("Выберите режим игры:",
                                     reply_markup=keyboard_choose_game_mode_xo)


async def process_invite_xo_game(callback: CallbackQuery, db, translator, size):
    user_id_one = callback.from_user.id
    logging.info(f"Пользователь 1: {user_id_one}")
    chat_info = await db.get_active_chat(user_id_one)
    logging.info(f"Информация об активном чате: {chat_info}")
    user_id_two = chat_info[1]

    user_one_message = await callback.message.edit_text(translator.get('send_request_for_game'),
                                                           reply_markup=keyboard_before_cancel_game_inline)

    user_two_message = await callback.bot.send_message(text=translator.get('get_game_request_xo'),
                                                          chat_id=user_id_two,
                                                          reply_markup=keyboard_before_accept_game_inline)

    await db.set_user_state(user_id_one, "waiting_for_start",
                            json.dumps({"message_id": user_one_message.message_id, "size": size}))
    await db.set_user_state(user_id_two, "waiting_for_start",
                            json.dumps({"message_id": user_two_message.message_id, "size": size}))

    logging.info(
        f"user message one: {user_one_message.message_id}, user message two: {user_two_message.message_id}")

    logging.info(f"Приглашение на игру отправлено от {user_id_one} к {user_id_two}")


@router.callback_query(F.data == "XO_mode_3", IsINChat())
async def process_invite_xo_game_3(callback: CallbackQuery, db, translator):
    await process_invite_xo_game(callback, db, translator, 3)


@router.callback_query(F.data == "XO_mode_4", IsINChat())
async def process_invite_xo_game_4(callback: CallbackQuery, db, translator):
    await process_invite_xo_game(callback, db, translator, 4)


@router.callback_query(F.data == "XO_mode_5", IsINChat())
async def process_invite_xo_game_5(callback: CallbackQuery, db, translator):
    await process_invite_xo_game(callback, db, translator, 5)


@router.callback_query(F.data == "accept_game", IsINChat(), DBStateFilter("waiting_for_start"))
async def process_accept_xo_game(callback: CallbackQuery, db, translator):
    user_id_one = callback.from_user.id
    chat_info = await db.get_active_chat(user_id_one)
    user_id_two = chat_info[1]

    user_two_message_info = await db.get_user_state(user_id_two)
    user_one_message_info = await db.get_user_state(user_id_one)

    user_two_message_id = json.loads(user_two_message_info['data']).get('message_id')
    user_one_message_id = json.loads(user_one_message_info['data']).get('message_id')
    size = json.loads(user_one_message_info['data']).get('size')

    # Создаем игру
    game = GameBoard(size)

    await db.set_user_state(user_id_one, "playing",
                            json.dumps({"message_id": user_one_message_id, "game": game.to_dict()}))

    await db.set_user_state(user_id_two, "playing",
                            json.dumps({"message_id": user_two_message_id, "game": game.to_dict()}))

    await callback.message.edit_text(translator.get('player_move', next_player="X"),
                                     reply_markup=game.get_board_markup())

    await callback.bot.edit_message_text(
        chat_id=user_id_two,
        message_id=user_two_message_id,
        text=translator.get('interlocutor_move', next_player="X"),
        reply_markup=game.get_board_markup()
    )

    await db.set_user_state(user_id_one, "player1_turn",
                            json.dumps({"message_id": user_one_message_id, "game": game.to_dict()}))


@router.callback_query(F.data == "cancel_game", IsINChat(), DBStateFilter("waiting_for_start"))
async def process_cancel_xo_game(callback: CallbackQuery, db, translator):
    user_id_one = callback.from_user.id
    chat_info = await db.get_active_chat(user_id_one)
    user_id_two = chat_info[1]

    user_two_message_info = await db.get_user_state(user_id_two)

    user_two_message_id = json.loads(user_two_message_info['data']).get('message_id')

    await callback.message.edit_text(translator.get('cancel_game'),
                                     reply_markup=None)

    await callback.bot.edit_message_text(
        chat_id=user_id_two,
        message_id=user_two_message_id,
        text=translator.get('cancel_game_interlocutor'),
        reply_markup=None
    )

    await db.clear_user_state(callback.from_user.id)
    await db.clear_user_state(chat_info[1])


@router.callback_query(F.data == "refuse_game", IsINChat(), DBStateFilter("waiting_for_start"))
async def process_refuse_xo_game(callback: CallbackQuery, db, translator):
    user_id_one = callback.from_user.id
    chat_info = await db.get_active_chat(user_id_one)
    user_id_two = chat_info[1]

    user_two_message_info = await db.get_user_state(user_id_two)

    user_two_message_id = json.loads(user_two_message_info['data']).get('message_id')

    await callback.message.edit_text(translator.get('refuse_game'),
                                     reply_markup=None)

    await callback.bot.edit_message_text(
        chat_id=user_id_two,
        message_id=user_two_message_id,
        text=translator.get('refuse_game_interlocutor'),
        reply_markup=None
    )

    await db.clear_user_state(callback.from_user.id)
    await db.clear_user_state(chat_info[1])
