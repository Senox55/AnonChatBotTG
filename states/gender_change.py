from aiogram.fsm.state import StatesGroup, State


class GenderChange(StatesGroup):
    waiting_for_gender = State()
