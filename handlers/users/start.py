import sqlalchemy
from aiogram import types
from aiogram.filters import CommandStart
from data.setting import async_session
from handlers.users import router
from keyboards.defaults.start_kb import kb
from sqlalchemy import select
from utils.db_api.sqlachemy_db import Users, ReferalLinks


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

@router.message(CommandStart(deep_link=True))
async def start(message: types.Message):
    async with async_session() as session:
        try:
            new_user: Users = Users(phone=None, username=message.from_user.username,
                                name=message.from_user.first_name,
                                tg_id=message.chat.id)
            session.add(new_user)
            await session.commit()
        except sqlalchemy.exc.IntegrityError:
            await message.answer('Вы уже пользуетесь ботом')
            await session.rollback()
            return

        user_who_invite_id = int(message.text.split()[1])

        query = select(Users).where(Users.telegram_id == user_who_invite_id)
        result = await session.execute(query)
        user_who_invite_data: Users = result.scalar_one_or_none()

        if user_who_invite_data == message.chat.id:
            await message.answer('Самого себя приглашать нельзя!!!')
            return

        ref_link_data: ReferalLinks = ReferalLinks(user_who_invite_id=user_who_invite_id, invited_user=message.chat.id)

        try:
            session.add(ref_link_data)
            await session.commit()
        except sqlalchemy.exc.IntegrityError:
            await message.answer("Вас уже пригласили")
            await session.rollback()

    #await message.answer("Привет, добро пожаловать в бота!\nПомощь - /help", reply_markup=kb)
    await message.answer(f"Привет, спасибо что пришел по приглашению от пользователя {user_who_invite_data.username}! /help", reply_markup=kb)


@router.message(CommandStart())
async def start(message: types.Message):
    async with async_session() as session:
        try:
            user: Users = Users(phone=None, username=message.from_user.username,
                                name=message.from_user.first_name,
                                tg_id=message.chat.id)
            session.add(user)
            await session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            await message.answer("Вы уже используете бота!")
            print(e)
            await session.rollback()
            return

    await message.answer("Привет, добро пожаловать в бота!\nПомощь - /help", reply_markup=kb)
    #await message.answer(f"Привет, спасибо что пришел по приглашению! /help", reply_markup=kb)
