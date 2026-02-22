from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def create_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отправить геолокацию', request_location=True)],
], resize_keyboard=True)