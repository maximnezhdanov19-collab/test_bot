import asyncio

from data.setting import dp, bot, engine
from utils.db_api.sqlachemy_db import Base
from utils.set_bot_commands import set_commands

blocked_count = 0

# Start polling

async def init_db():
    async with engine.begin() as conn:
        print('Создана таблица', list(Base.metadata.tables.keys()))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def on_startup():
    await init_db()
    print('Бот был запущен!')
    # db.clear_orders_table()
    # db.create_table_orders()


async def main():
    dp.startup.register(set_commands)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
