from aiogram.fsm.state import StatesGroup, State


class GameStates(StatesGroup):
    waiting_for_start = State()
    playing = State()
    player1_turn = State()
    player2_turn = State()
    game_over = State()
