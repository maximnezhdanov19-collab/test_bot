from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_inline(games: dict[str, str]):
    builder = InlineKeyboardBuilder()
    for key, value in games.items():
        builder.button(text=value.get('title'), callback_data=f'gameTest_{key}')
    builder.button(text='Отмена', callback_data='help')
    builder.adjust(2, 2, 1)
    return builder.as_markup()