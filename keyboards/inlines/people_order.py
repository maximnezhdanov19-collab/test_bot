from aiogram.utils.keyboard import InlineKeyboardBuilder

list_of_builders = []

builder_1 = InlineKeyboardBuilder()
builder_1.button(text='1', callback_data='OPListalka_1')
builder_1.button(text='2', callback_data='OPListalka_2')
builder_1.button(text='3', callback_data='OPListalka_3')
builder_1.button(text='4', callback_data='OPListalka_4')
builder_1.button(text='5', callback_data='OPListalka_5')
builder_1.button(text='➡️', callback_data='oplist➡️')
builder_1.button(text='Назад', callback_data='make_order_back')
builder_1.adjust(6, 1)
list_of_builders.append(builder_1)

builder = InlineKeyboardBuilder()
builder.button(text='⬅️', callback_data='oplist⬅️')
builder.button(text='6', callback_data='OPListalka_6')
builder.button(text='7', callback_data='OPListalka_7')
builder.button(text='8', callback_data='OPListalka_8')
builder.button(text='9', callback_data='OPListalka_9')
builder.button(text='10', callback_data='OPListalka_10')
builder.button(text='Назад', callback_data='make_order_back')
builder.adjust(6, 1)
list_of_builders.append(builder)

list_of_builders.append(builder_1)
