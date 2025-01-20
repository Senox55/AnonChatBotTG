from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
import json
import logging

from filters.db_state_filter import DBStateFilter
from games.game_xo import GameBoard
from states.game_xo import GameStates
from filters.is_in_chat_filter import IsINChat
from keyboards import *

logging.basicConfig(level=logging.INFO)

router = Router()


async def process_move(callback: CallbackQuery, db, translator, current_player):
    user_id_one = callback.from_user.id
    user_state_one = await db.get_user_state(user_id_one)
    user_data_one = json.loads(user_state_one['data'])

    chat_info = await db.get_active_chat(user_id_one)

    user_id_two = chat_info[1]
    user_state_two = await db.get_user_state(user_id_two)
    user_data_two = json.loads(user_state_two['data'])

    user_two_message_id = user_data_two.get('message_id')
    user_one_message_id = user_data_one.get('message_id')
    game = GameBoard.from_dict(user_data_one.get('game'))
    logging.info(f"Game: {game}, opponent_message_id: {user_two_message_id}, user_id_two {user_id_two}")

    data = callback.data

    if data.startswith("move_"):
        position = int(data.split("_")[1])

        if game.make_move(position):
            if game.winner:
                board_text = game.get_board_text()
                final_text = translator.get('finish_game_xo', winner_text=game.winner, board_text=board_text)
                # Обновляем сообщение у текущего игрока
                await callback.message.edit_text(
                    text=final_text, parse_mode="MarkdownV2"
                )
                # Обновляем сообщение у второго игрока
                if user_two_message_id:
                    await callback.bot.edit_message_text(
                        chat_id=user_id_two,
                        message_id=user_two_message_id,
                        text=final_text, parse_mode="MarkdownV2"
                    )

                await db.clear_user_state(user_id_one)
                await db.clear_user_state(user_id_two)
            else:
                next_player = "O" if current_player == "X" else "X"
                # Обновляем сообщение у текущего игрока
                await callback.message.edit_text(
                    text=translator.get('move_player', next_player=next_player),
                    reply_markup=game.get_board_markup()
                )

                # Обновляем сообщение у второго игрока
                if user_two_message_id:
                    await callback.bot.edit_message_text(
                        chat_id=user_id_two,
                        message_id=user_two_message_id,
                        text=translator.get('move_player', next_player=next_player),
                        reply_markup=game.get_board_markup()
                    )
                    player_turn = "player2_turn" if next_player == 'O' else "player1_turn"
                    await db.set_user_state(user_id_one, "playing",
                                            json.dumps({"message_id": user_one_message_id,
                                                        "game": game.to_dict()}))

                    await db.set_user_state(user_id_two, player_turn,
                                            json.dumps({"message_id": user_two_message_id,
                                                        "game": game.to_dict()}))
        else:
            await callback.answer(translator.get('illegal_move'))
    elif data == "ignore":
        await callback.answer(translator.get('cannot_click_cell'))


@router.callback_query(DBStateFilter("player1_turn"), IsINChat())
async def process_player1_turn(callback_query: CallbackQuery, db, translator):
    await process_move(callback_query, db, translator, current_player="X")


@router.callback_query(DBStateFilter("player2_turn"), IsINChat())
async def process_player2_turn(callback_query: CallbackQuery, db, translator):
    await process_move(callback_query, db, translator, current_player="O")
