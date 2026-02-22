import aiogram
from aiogram import types
from aiogram.filters import Command
from data.setting import bot, dp
from handlers.users import router
from aiogram import F
from time import sleep
from keyboards.defaults.start_kb import kb

process = ['Начинаем взлом...',
           '[○○○○○○○○○○] 0%',
           '[■○○○○○○○○○] 10%',
           '[■■○○○○○○○○] 20%',
           '[■■■○○○○○○○] 30%',
           '[■■■■○○○○○○] 40%',
           '[■■■■■○○○○○] 50%',
           '[■■■■■■○○○○] 60%',
           '[■■■■■■■○○○] 70%',
           '[■■■■■■■■○○] 80%',
           '[■■■■■■■■■○] 90%',
           '[■■■■■■■■■■] 100%',
           'Ваш аккаунт был успешно взломан!']

@router.message(Command("hacking"))
async def start(message: types.Message):
    chat = await bot.get_chat(chat_id=message.chat.id)
    user_data = (f'ID сообщения: {message.message_id}\n'
                 f'ID чата: {chat.id}\n'
                 f'Фамилия: {chat.last_name}\n'
                 f'Имя: {chat.first_name}\n'
                 f'Тип чата: {chat.type}\n'
                 f'ID: {message.from_user.id}'
                 f'Ну а дальше лень взламывать')
    process.append(user_data)
    await message.answer(text=process[0])
    sleep(1)
    message_id = message.message_id + 1
    for string in process:
        if string != process[0]:
            await bot.edit_message_text(message_id=message_id, chat_id=message.chat.id, text=string)