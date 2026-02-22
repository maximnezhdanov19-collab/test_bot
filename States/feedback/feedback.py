from aiogram.fsm.state import StatesGroup, State

class FeedBack(StatesGroup):
    phone = State()
    text = State()