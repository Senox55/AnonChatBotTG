from aiogram.fsm.state import StatesGroup, State


class RegistrationFSM(StatesGroup):
    fill_gender = State()
    fill_age = State()
