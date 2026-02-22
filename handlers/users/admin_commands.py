import aiogram
from aiogram import types, F
from aiogram.filters import Command
from data.setting import bot, dp
from handlers.users import router
from keyboards.defaults.start_kb import kb
from filters.admin_filter import IsAdmin
from middlewares.all_in_one import admin

from data.setting import async_session
from sqlalchemy import select
from utils.db_api.sqlachemy_db import Admins

async def select_admins():
    async with async_session() as session:
        query = select(Admins)
        result = await session.execute(query)
        admins: list[Admins] = result.scalars().all()
        return admins


@router.message(Command('admin'))
async def admin_function(message: types.Message):
    await message.answer(
            text='<b>Поздравляем!</b> Теперь вы админ!',
            parse_mode='HTML')
    async with async_session() as session:
        admins = await select_admins()
        if message.from_user.id not in [admin.user.telegram_id for admin in admins]:
            admin: Admins = Admins(user_id=message.from_user.id)
            session.add(admin)
            await session.commit()


