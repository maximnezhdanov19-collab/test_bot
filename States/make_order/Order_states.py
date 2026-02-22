from aiogram.fsm.state import StatesGroup, State

class Order(StatesGroup):
    people_count = State()
    time = State()
    tariff = State()
    contacts = State()
    yandex_map = State()