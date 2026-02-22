import io

import aiogram
from aiogram import types
from aiogram.filters import Command

from handlers.group import group_router


@group_router.message(Command('start'))
async def set_title(message: types.Message):
    await message.answer('Это /start группы')

@group_router.message(Command('set_photo'))
async def set_title(message: types.Message, bot: aiogram.Bot):
    photo = message.reply_to_message.photo[-1]
    photo_file = io.BytesIO()
    await bot.download(photo.file_id, destination=photo_file)
    await message.chat.set_photo(photo=photo_file.name)

@group_router.message(Command('set_title'))
async def set_title(message: types.Message):
    text = message.reply_to_message.text
    await message.chat.set_title(title=text)



