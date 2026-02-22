import logging

from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from filters.is_chat import IsChat
from filters.is_group import IsGroup
from middlewares.all_in_one import AllInOne
import os, dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PASSWORD = os.getenv("PASSWORD")
DATABASE_URL = rf'{os.getenv("DATABASE_URL")}'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

engine = create_async_engine(url=DATABASE_URL, echo=False)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

from handlers.users import router as user_router
from handlers.group import group_router

dp.include_router(group_router)
dp.include_router(user_router)
group_router.message.filter(IsGroup())

# dp.update.middleware(AllInOne())

