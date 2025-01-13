from aiogram.fsm.state import StatesGroup, State


class AgeChange(StatesGroup):
    waiting_for_age = State()
