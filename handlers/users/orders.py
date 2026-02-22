from aiogram import types
from aiogram import types
from aiogram.filters import Command
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from data.setting import async_session
from handlers.users import router
from utils.db_api.sqlachemy_db import Orders


@router.message(Command("view_orders"))
async def orders(message: types.Message):
    async with async_session() as session:
        query = select(Orders).options(selectinload(Orders.user))
        result = await session.execute(query)
        orders: list[Orders] = result.scalars().all()
        for order in orders:
            text = (f"Телефон: {order.user.phone}\nКол-во людей: {order.people_count}\n"
                    f"Тариф: {order.tariff}\nID: {order.id}\nВремя: {order.order_time}")
            await message.answer(text=text)
        await session.commit()
