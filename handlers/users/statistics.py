from aiogram import types, F
from aiogram.types import ChatMemberUpdated
from data.setting import bot, dp
from handlers.users import router
from aiogram.filters import Command, ChatMemberUpdatedFilter, KICKED
from aiogram import exceptions
from app import blocked_count

from data.setting import async_session
from sqlalchemy import select, Boolean
from sqlalchemy.orm import selectinload
from utils.db_api.sqlachemy_db import Users, Orders, ReferalLinks

list_of_blocked_id = []

async def select_order():
    async with async_session() as session:
        query = select(Orders)
        result = await session.execute(query)
        orders: list[Orders] = result.scalars().all()
        return orders

async def select_users():
    async with async_session() as session:
        query = select(Users)
        result = await session.execute(query)
        users: list[Users] = result.scalars().all()
        return users

async def select_reflinks():
    async with async_session() as session:
        query = select(ReferalLinks)
        result = await session.execute(query)
        reflinks: list[ReferalLinks] = result.scalars().all()
        return reflinks

@router.message(Command("statistic"))
async def statistic(message: types.Message):
    users = await select_users()
    users = len(users)

    messages = message.message_id

    await message.answer(text = f"Всего отправлено сообщений: {messages} \n"
                                f"Всего пользователей: {users} \n"
                                f"Пользователей заблокировавших бота: {len(list_of_blocked_id)} \n"
                                f"Заказов: {len(await select_order())}\n"
                                f"Приглашено: {len(await select_reflinks())}")


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated):
    print("blocked")
    async with async_session() as session:
        id = event.from_user.id
        query = select(Users).where(Users.telegram_id == id)
        result = await session.execute(query)
        user: Users = result.scalar_one_or_none()
        user.is_active = True
        await session.commit()
        print('Пользователь заблокал бота и его добавили в базе данных')


