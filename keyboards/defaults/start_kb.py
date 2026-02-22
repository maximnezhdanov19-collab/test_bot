from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Котики'), KeyboardButton(text='Викторина')],
    [KeyboardButton(text='Помощь!')]
], resize_keyboard=True)