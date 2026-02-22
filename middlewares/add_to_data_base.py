from aiogram import BaseMiddleware
from aiogram import types

from data.setting import async_session
from sqlalchemy import select
from utils.db_api.sqlachemy_db import Users


async def select_users():
    async with async_session() as session:
        query = select(Users)
        result = await session.execute(query)
        users: list[Users] = result.scalars().all()
        return users


class AddToDB(BaseMiddleware):

    async def on_pre_process_update(self, update: types.Update, data: dict) -> None:
        async with async_session() as session:
            users = await select_users()
            print(users)


            if update.message == None and update.callback_query != None:
                update = update.callback_query

            if update.message.from_user.id not in [user.telegram_id for user in users]:
                print('===========')
                print([user.telegram_id for user in users])
                print('===========')
                user: Users = Users(phone=None, username=update.message.from_user.username, name=update.message.from_user.first_name,
                                tg_id=update.message.chat.id)
                session.add(user)
                await session.commit()

            users = await select_users()
            print(users)

        print("Новый апдейт")

    async def __call__(self, handler, event: types.Update, data: dict):
        await self.on_pre_process_update(event, data)

        responce = await handler(event, data)
        return responce

