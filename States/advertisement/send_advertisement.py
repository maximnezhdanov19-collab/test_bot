from aiogram.fsm.state import StatesGroup, State

class Advertisement(StatesGroup):
    photo = State()
    text = State()
    site = State()
    end = State()