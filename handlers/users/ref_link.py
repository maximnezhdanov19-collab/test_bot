import aiogram
from aiogram import types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data.setting import bot, dp
from handlers.users import router
from aiogram.utils.deep_linking import create_start_link
from keyboards.defaults.start_kb import kb

@router.message(Command('ref_link'))
async def ref_link(mess: types.Message):
    link = await create_start_link(bot, payload=str(mess.from_user.id))
    await mess.answer(text=f'Вот твоя ссылка: {link}')