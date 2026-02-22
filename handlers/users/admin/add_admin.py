from aiogram import types
from aiogram.filters import Command
from sqlalchemy import select

from data.setting import async_session, PASSWORD
from handlers.users import router

from utils.db_api.sqlachemy_db import Users, Admins


@router.message(Command("admin_cmd"))
async def admin_cmd(message: types.Message):
    password = message.text.split()
    if len(password) == 1:
        await message.answer("Введите пароль!")
        return
    password = password[-1]


    if password == PASSWORD:
        async with async_session() as session:

            admin: Admins = Admins(user_id=message.chat.id)
            session.add(admin)
            await session.commit()
            await message.answer("Теперь вы админ!")
    else:
        await message.answer("Пароль неверный!")


@router.message(Command("add_admin"))
async def add_admin(message: types.Message):
    id = message.text.split()
    if len(id) == 1:
        await message.answer("Введите ID!")
        return

    id = id[-1]

    async with async_session() as session:

        try:
            admin: Admins = Admins(user_id=int(id))
            session.add(admin)
            await session.commit()
            await message.answer("Админ добавлен!")

        except:
            await message.answer("Это уже админ!")
