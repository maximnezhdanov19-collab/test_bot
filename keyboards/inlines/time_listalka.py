from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_kb(hour: str):
    builder = InlineKeyboardBuilder()
    next_hour = int(hour) + 1
    prev_hour = int(hour) - 1

    builder.button(text = f'⬅️', callback_data=f'MakeOrderTimeBack_{prev_hour}')
    builder.button(text = f'{hour}:00', callback_data=f'MakeOrderTime_{hour}:00')
    builder.button(text=f'{hour}:30', callback_data=f'MakeOrderTime_{hour}:30')
    builder.button(text=f'➡️', callback_data=f'MakeOrderTimeNext_{next_hour}')
    builder.button(text='Назад', callback_data='make_order_back')

    builder.adjust(4, 1)

    return builder.as_markup()

