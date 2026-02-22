import aiogram
from aiogram import types
from aiogram.filters import Command
from data.setting import bot, dp
from handlers.users import router
from aiogram import F
from keyboards.defaults.start_kb import kb

@router.message(Command('help'))
@router.message(F.text == 'Помощь!')
async def help(message: types.Message):
    await message.answer('''<b>📝 Вот все что может бот:</b>
    
/quiz - Викторина по ЯП 👩‍🏫

/game_clubs - Посмотреть компьютерные клубы 🖥️

/make_order - Сделать заказ в клуб 💌

/feedback - Обратная связь 💬

Также в боте есть ехо 🗣️

Открыта дефолтная клавиатура!

''', reply_markup=kb, parse_mode='HTML')

@router.callback_query(F.data == 'help')
async def help_callback(callback: types.CallbackQuery):
    await callback.answer()
    await help(callback.message)