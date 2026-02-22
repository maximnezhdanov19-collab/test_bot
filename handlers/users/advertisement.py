from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from data.setting import async_session, bot
from handlers.users import router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from States.advertisement.send_advertisement import Advertisement
from utils.db_api.sqlachemy_db import Users, Admins
from handlers.users.help import help


async def select_users():
    async with async_session() as session:
        query = select(Users)
        result = await session.execute(query)
        users: list[Users] = result.scalars().all()
        return users

async def select_admins():
    async with async_session() as session:
        query = select(Admins)
        result = await session.execute(query)
        admins: list[Admins] = result.scalars().all()
        return admins

@router.callback_query(Advertisement.photo, F.data == 'AdBackTo_help')
async def Back_help(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await help(call.message)
    await state.clear()


@router.callback_query(Advertisement.text, F.data == 'AdBackTo_photo')
async def Back_photo(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer()
    await advertisement(call.message, state)

@router.callback_query(Advertisement.site, F.data == 'AdBackTo_text')
async def Back_text(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer()
    await advertisement_photo(call.message, state)



@router.message(Command("advertisement"))
async def advertisement(message: types.Message, state: FSMContext):
    async with async_session() as session:
        admins = await select_admins()
        if message.from_user.id in [admin.user_id for admin in admins]:
            await state.update_data(id=message.chat.id)
            await state.update_data(message=message)
            await state.set_state(Advertisement.photo)
            builder = InlineKeyboardBuilder()
            builder.button(text='Назад', callback_data='AdBackTo_help')
            await message.answer(text="Отправьте ссылку на фотографию для рекламы", reply_markup=builder.as_markup())
        else:
            await message.answer(text='Вы не админ')


@router.message(Advertisement.photo)
async def advertisement_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.text)
    await state.set_state(Advertisement.text)
    builder = InlineKeyboardBuilder()
    builder.button(text='Назад', callback_data='AdBackTo_photo')
    await message.answer(text="Отправьте текст для рекламы", reply_markup=builder.as_markup())


@router.message(Advertisement.text)
async def advertisement_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(Advertisement.site)
    builder = InlineKeyboardBuilder()
    builder.button(text='Назад', callback_data='AdBackTo_text')
    await message.answer(text="Отправьте ссылку на сайт для кнопки на вашей рекламе", reply_markup=builder.as_markup())


@router.message(Advertisement.site)
async def advertisement_site(message: types.Message, state: FSMContext):
    await state.update_data(site=message.text)
    await state.set_state(Advertisement.end)

    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    site = data.get('site')
    admin_id = data.get('id')

    builder = InlineKeyboardBuilder().button(text='Подробнее', url=site)
    if len(text) < 1024:
        await message.answer_photo(caption=text, photo=photo, reply_markup=builder.as_markup())
    else:
        await message.answer_photo(photo=photo)
        await message.answer(reply_markup=builder.as_markup(), text=text)

    builder = InlineKeyboardBuilder()
    builder.button(text='Да', callback_data='send_reclama')
    builder.button(text='Нет', callback_data='help')
    await message.answer(text="Отправить вашу рекламу???", reply_markup=builder.as_markup())


@router.callback_query(Advertisement.end, F.data == "send_reclama")
async def advertisement_end(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    site = data.get('site')
    admin_id = data.get('id')
    users = await select_users()
    users_id = [user.telegram_id for user in users]
    builder = InlineKeyboardBuilder().button(text='Подробнее', url=site)
    await state.clear()

    for id in users_id:
        if len(text) < 1024:
            await bot.send_photo(chat_id=id, caption=text, parse_mode='HTML', photo=photo, reply_markup=builder.as_markup())
        else:
            await bot.send_photo(chat_id=id, photo=photo)
            await bot.send_message(reply_markup=builder.as_markup(), text=text, chat_id=id)

    await bot.send_message(chat_id=admin_id, text='Сообщение отправлено по всем пользователям!!!')