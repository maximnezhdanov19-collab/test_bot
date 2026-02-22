import aiogram
from aiogram import types, F
from aiogram.filters import Command
from data.setting import bot, dp
from handlers.users import router
from keyboards.defaults.start_kb import kb
import json

@router.message(F.voice)
async def voice(voice: types.Message):
    voice_json = voice.voice.json()
    voice_data = json.loads(voice_json)

    file_size = voice_data.get('file_size')
    file_id = voice_data.get('file_id')
    duration = voice_data.get('duration')

    await voice.answer(text=f'<b>Инфо о голосовом:</b>\n\nРазмер: <i>{file_size}</i>\n\nАйдишник: <i>{file_id}</i>\n\nПродолжительность: <i>{duration}</i>', parse_mode='HTML', reply_markup=kb)

@router.message(F.photo)
async def photo(mess: types.Message):
    await bot.send_photo(photo=mess.photo[-1].file_id, chat_id=mess.from_user.id, reply_markup=kb)

@router.message()
async def echo(message: types.Message):
    text = message.text
    await message.answer(text, reply_markup=kb)

# @router.callback_query()
# async def start(callback: types.CallbackQuery):
#     await callback.answer("")
#     data = callback.data
#     await callback.message.answer(f'Не отловлен callback: {data}', reply_markup=kb)
