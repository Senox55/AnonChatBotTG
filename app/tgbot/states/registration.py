from aiogram.fsm.state import StatesGroup, State


class RegistrationFSM(StatesGroup):
    FILL_GENDER = State()
    FILL_AGE = State()
