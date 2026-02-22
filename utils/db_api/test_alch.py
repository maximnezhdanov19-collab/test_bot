import asyncio
from random import randint, choice
from utils.db_api.sqlachemy_db import Orders

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, selectinload

from utils.db_api.sqlachemy_db import Users, Base

DATABASE_URL = "sqlite+aiosqlite:///./main.db"

engine = create_async_engine(url=DATABASE_URL, echo=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        print('Создана таблица', list(Base.metadata.tables.keys()))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def add_value(phone, username, name, tg_id):
    async with async_session() as session:
        user = Users(phone=phone, username=username, name=name, tg_id=tg_id)
        session.add(user)
        await session.commit()

async def add_order():
    async with async_session() as session:
        user: Users = Users(phone='8800555352', username="maxnezhd", name='Maxim', tg_id=4567)
        session.add(user)
        await session.commit()
        order: Orders = Orders(user_id=user.id, people_count=2, order_time='8:00', tariff='Buis')
        print(order)
        session.add(order)
        await session.commit()


async def select_users():
    async with async_session() as session:
        query = select(Users)
        result = await session.execute(query)
        users: list[Users] = result.scalars().all()
        print(users[0].username)
        print(users)
        return users


async def select_order():
    async with async_session() as session:
        query = select(Orders).options(selectinload(Orders.user))
        result = await session.execute(query)
        orders: list[Orders] = result.scalars().all()
        for order in orders:
            print(order.user)
        await session.commit()


def generate():
    phone = f'+7 {randint(900, 999)} {randint(100, 999)} {randint(10, 99)} {randint(10, 99)}'
    symbols = 'qwertyuiopasdfghjklzxcvbnm_1234567890'
    symbols += 'qwertyuiopasdfghjklzxcvbnm'.upper()
    username = f'@{''.join([choice(symbols) for i in range(randint(4, 10))])}'
    all_symbols = symbols + 'йцукенгшщзхъфывапролджэячсмитьбю' + 'йцукенгшщзхъфывапролджэячсмитьбю'.upper()
    name = f'{''.join([choice(all_symbols) for i in range(randint(4, 10))])}'
    return phone, username, name


async def add(num: int):
    for i in range(num):
        data = generate()
        await add_value(data[0], data[1], data[2], randint(10000, 10000000))


async def main():
    await init_db()
    await add(10)
    await add_order()
    await select_order()
    await select_users()


asyncio.run(main())
