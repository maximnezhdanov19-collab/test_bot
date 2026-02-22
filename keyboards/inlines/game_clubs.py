from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_inline(clubs: list[dict]):
    builder = InlineKeyboardBuilder()
    for club in clubs:
        builder.button(text=club.get('name'), callback_data=club.get('callback'))

    builder.button(text='Отмена', callback_data='help')
    builder.adjust(3, 3, 3, 1)
    return builder.as_markup()

def create_inline2(clubs: list[dict], callback):
    dict = [
        {'text': 'VIP зона',
         'callback':'VIP_'},
        {'text': 'Компьютеры',
         'callback': 'Comps_'},
        {'text': 'Напитки',
         'callback': 'Drinks_'}
    ]
    builder = InlineKeyboardBuilder()
    for club in clubs:
        builder.button(text=club.get('name'), callback_data=club.get('callback'))
    for butt in dict:
        builder.button(text=butt.get('text'), callback_data=butt.get('callback') + callback)
    builder.button(text='Отмена', callback_data='help')
    builder.adjust(3, 3, 3, 1)
    return builder.as_markup()