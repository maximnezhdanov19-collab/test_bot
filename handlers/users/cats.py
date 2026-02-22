from aiogram import F
from aiogram import types
from aiogram.filters import Command
from data.setting import bot, dp
from handlers.users import router
from random import randint
from keyboards.defaults.start_kb import kb

@router.message(F.text.lower() == 'котики')
async def command_random_cats(message: types.Message):
    photo_url = f'https://cataas.com/cat?{randint(1, 10000)}'
    await bot.send_photo(chat_id=message.chat.id, photo=photo_url, reply_markup=kb)