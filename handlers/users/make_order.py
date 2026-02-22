from io import BytesIO

import sqlalchemy.exc
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from sqlalchemy import select

from data.setting import async_session

from data.setting import bot, dp
from handlers.users import router
from aiogram import F
from aiogram.fsm.context import FSMContext
from States.make_order.Order_states import Order
from keyboards.inlines.people_order import list_of_builders
from keyboards.inlines.time_listalka import create_kb
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputFile

from handlers.users.help import help

from utils.db_api.sqlachemy_db import Users, Orders
from keyboards.defaults.location_kb import create_keyboard


users_index_people = {}


@router.message(Command('make_order'))
async def start_order(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text='Повторить заказ', callback_data='repeat_order')
    builder.button(text='Новый заказ', callback_data='new_order')
    builder.button(text='Назад', callback_data='help')
    builder.adjust(2, 1)
    await message.answer(text='Выберите следующее действие:', reply_markup=builder.as_markup())


@router.callback_query(Order.people_count, F.data == 'make_order_back')
async def people_count_back(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await help(callback.message)
    await state.clear()


@router.callback_query(Order.time, F.data == 'make_order_back')
async def time_back(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await make_order(callback, state)


@router.callback_query(Order.tariff, F.data == 'make_order_back')
async def tariff_back(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await time(callback, state, with_back=True)


@router.callback_query(Order.tariff, F.data == 'make_order_back')
async def contacts_back(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await tariff()


@router.callback_query(F.data == 'repeat_order')
async def repeat_order(callback: types.CallbackQuery):
    message = callback.message
    async with async_session() as session:
        query = select(Users).where(Users.telegram_id == message.from_user.id)
        query2 = select(Orders).where(Orders.user_id == Users.id)

        result = await session.execute(query)
        result2 = await session.execute(query2)

        user: Users = result.scalar_one_or_none()
        last_order: Orders = result2.scalar_one_or_none()

        order: Orders = Orders(user_id=last_order.user_id, people_count=last_order.people_count,
                               order_time=last_order.order_time, tariff=last_order.tariff)
        session.add(order)
        await session.commit()

    await message.answer(text=f'''Новый заказ:

Количество людей: {last_order.people_count}

Время: {last_order.order_time}

Тариф: {last_order.tariff}

Контакты: {user.phone}''')


@router.callback_query(F.data == 'new_order')
async def make_order(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(message=callback.message)
    if callback.message.chat.id not in users_index_people:
        users_index_people.update({callback.message.chat.id: 0})
    await callback.message.edit_text(text='Выберите количество человек',
                                     reply_markup=list_of_builders[
                                         users_index_people.get(callback.message.chat.id)].as_markup())
    await state.set_state(Order.people_count)


@router.callback_query(Order.people_count, F.data.startswith('oplist'))
async def enter_people(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'oplist⬅️':
        users_index_people[callback.message.chat.id] -= 1
    else:
        users_index_people[callback.message.chat.id] += 1
    await callback.message.edit_reply_markup(
        reply_markup=list_of_builders[users_index_people.get(callback.message.chat.id)].as_markup())
    await state.set_state(Order.people_count)


@router.callback_query(Order.people_count, F.data.startswith('OPListalka_'))
async def time(callback: types.CallbackQuery, state: FSMContext, with_back=False):
    await state.set_state(Order.time)
    await callback.answer()
    if not with_back:
        people = int(callback.data.split('_')[1])
        await state.update_data(people_count=people)
    await callback.message.edit_text(text='Выберите время: ',
                                     reply_markup=create_kb(hour='9'))


@router.callback_query(Order.time, F.data.startswith('MakeOrderTimeNext'))
async def make_order_time_next(callback: types.CallbackQuery, state: FSMContext):
    hour = int(callback.data.split('_')[-1])
    if hour > 23:
        hour = 9
    await callback.message.edit_reply_markup(reply_markup=create_kb(hour=str(hour)))
    await state.set_state(Order.time)


@router.callback_query(Order.time, F.data.startswith('MakeOrderTimeBack'))
async def make_order_time_back(callback: types.CallbackQuery, state: FSMContext):
    hour = int(callback.data.split('_')[-1])
    if hour < 9:
        hour = 23
    await callback.message.edit_reply_markup(reply_markup=create_kb(hour=str(hour)))
    await state.set_state(Order.time)


@router.callback_query(Order.time, F.data.startswith('MakeOrderTime_'))
async def tariff(callback: types.CallbackQuery, state: FSMContext):
    time = callback.data.split('_')[1]
    await callback.answer()
    await state.update_data(time=time)
    builder = InlineKeyboardBuilder()
    builder.button(text='Фиксированный', callback_data='tariff_Фиксированный')
    builder.button(text='Пакетный', callback_data='tariff_Пакетный')
    builder.button(text='Поминутный', callback_data='tariff_Поминутный')
    builder.button(text='Несгораемый', callback_data='tariff_Несгораемый')
    builder.button(text='Назад', callback_data='make_order_back')
    builder.adjust(2, 2, 1)
    await callback.message.edit_text(text='Выберите тариф:', reply_markup=builder.as_markup())
    await state.set_state(Order.tariff)


@router.callback_query(Order.tariff, F.data.startswith('tariff_'))
async def contacts(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Order.contacts)
    tariff = callback.data.split('_')[1]
    await callback.answer()
    await state.update_data(tariff=tariff)
    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить контакт', request_contact=True)]],
                                 resize_keyboard=True, one_time_keyboard=True)
    await callback.message.answer(text='Нажмите на кнопку чтобы отправить контакт', reply_markup=markup)


@router.message(Order.contacts, F.contact)
async def contacts(message: types.Message, state: FSMContext):
    contact = message.contact.phone_number
    await state.update_data(contact=contact)
    data = await state.get_data()
    message = data.get('message')
    people_count = data.get('people_count')
    tariff = data.get('tariff')
    time = data.get('time')
    contacts = data.get('contact')
    await message.answer(text=f'''Новый заказ:

Количество людей: {people_count}
 
Время: {time}

Тариф: {tariff}

Контакты: {contacts}''')

    async with async_session() as session:
        try:
            user: Users = Users(phone=contact, username=message.chat.username, name=message.chat.first_name,
                                tg_id=message.chat.id)
            session.add(user)
            await session.commit()
        except sqlalchemy.exc.IntegrityError:
            await session.rollback()
        order: Orders = Orders(user_id=message.chat.id, people_count=people_count, order_time=time, tariff=tariff)
        session.add(order)
        await session.commit()

    await message.answer(text='Отправьте геолокацию для маршрута', reply_markup=create_keyboard())
    await state.set_state(Order.yandex_map)

    # db.add_order(people_count=people_count, time=time, tariff=tariff, contacts=contact, username=message.chat.username, name=message.from_user.first_name)


@router.message(F.location, Order.yandex_map)
async def location(message: types.Message, state: FSMContext):
    lat_club, lon_club = 45.044183, 38.975375
    lat_user, lon_user = message.location.latitude, message.location.longitude

    yandex_maps = f"https://yandex.ru/maps?rtext={lat_user},{lon_user}~{lat_club},{lon_club}"

    await message.answer(text=f"Ваш заказ готов! Маршрут до клуба: <a href='{yandex_maps}'>Жми</a>", parse_mode='HTML')
    await state.clear()

    bot_info = await bot.get_me()
    bot_username = bot_info.username

    url = f"https://t.me/{bot_username}?start=order_info-{order_info.id}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )


    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    await message.answer_photo(caption=f"Этот QR-code нужно показать администратору на входе {url}",
                               photo=InputFile(buffer, filename="qr_code.png")
                          )
