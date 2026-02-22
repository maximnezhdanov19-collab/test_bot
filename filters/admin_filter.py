from aiogram.filters import BaseFilter
from aiogram.types import Message

from data.setting import async_session
from utils.db_api.sqlachemy_db import Users, Admins
from sqlalchemy import select


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        tg_id = message.from_user.id
        async with async_session() as session:
            query = select(Admins).where(Users.telegram_id == tg_id).join(Users)
            result = await session.execute(query)
            admin: Admins = result.scalar_one_or_none()

        return admin is not None
