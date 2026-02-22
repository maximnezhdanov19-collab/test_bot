from aiogram import types, F
from aiogram.filters import Command
from data.setting import async_session, bot
from handlers.users import router
from States.feedback.feedback import FeedBack
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy import select
from utils.db_api.sqlachemy_db import Users, Admins

async def select_admins():
    async with async_session() as session:
        query = select(Admins)
        result = await session.execute(query)
        admins: list[Admins] = result.scalars().all()
        return admins


@router.message(Command("feedback"))
async def feedback(message: types.Message, state: FSMContext):
    id = message.chat.id
    username = message.chat.username
    await state.update_data(id=id)
    await state.update_data(username=username)
    await state.set_state(FeedBack.phone)

    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Отправить номер телефона', request_contact=True)],
    ], resize_keyboard=True)

    await message.answer(text='Нажмите на кнопку на клавиатуре, чтобы отправить контакт', reply_markup=kb)


@router.message(FeedBack.phone)
async def feedback(message: types.Message, state: FSMContext):
    try:
        phone = message.contact.phone_number
    except:
        await message.answer(text='Нажмите на кнопку')
        return

    await state.update_data(phone=phone)
    await state.set_state(FeedBack.text)

    await message.answer(text='Отправьте обратную связь')


@router.message(FeedBack.text)
async def feedback(message: types.Message, state: FSMContext):

    data = await state.get_data()
    phone = data['phone']
    username = data['username']
    id = data['id']

    await message.answer(text='Обратная связь отправлен всем админам!')

    await state.clear()

    text = f"<b>Обратная связь!!!</b>\n\nТелефон: {phone}\n\nИмя: @{username}\n\nID: {id}\n\nОбратная связь: {message.text}"

    admins = await select_admins()
    for i in range(len(admins)):
        await bot.send_message(chat_id=admins[i].user_id, text=text, parse_mode='HTML')