import aiogram
from aiogram import types, F
from aiogram.filters import Command
from data.setting import bot, dp
from handlers.users import router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from States.quiz.Quiz_state import Quiz
from aiogram.fsm.context import FSMContext
from get_answers import quiz_answers
from keyboards.defaults.start_kb import kb

@router.callback_query(Quiz.QS, F.data == 'start_quiz')
async def first_question_quiz(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    await callback.answer()

    for answer in quiz_answers[0].get('answer'):
        builder.button(text=answer, callback_data='Quiz-0-_'+answer)
    builder.adjust(5)

    await callback.message.answer(text=quiz_answers[0].get('question'), reply_markup=builder.as_markup())


@router.message(F.text == 'Викторина')
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message, state: FSMContext):
    await state.update_data(right_answers=0)
    await state.set_state(Quiz.QS)
    builder = InlineKeyboardBuilder()
    builder.button(text='Начать', callback_data='start_quiz')
    builder.button(text='Выйти', callback_data='help')
    builder.adjust(2)
    await message.answer(text='📚🤪 Вы попали на викторину, хотите начать?', reply_markup=builder.as_markup())


@router.callback_query(Quiz.QS, F.data.startswith('Quiz'))
async def questions(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Quiz.QS)
    question_number = int(callback.data.split('-')[1])
    user_answer = callback.data.split('_')[1]
    right_answer = quiz_answers[question_number].get('right_answer')
    await callback.message.delete()

    builder = InlineKeyboardBuilder()
    if quiz_answers[-1].get('question') != quiz_answers[question_number].get('question'):
        builder.button(text='Следующий вопрос', callback_data='next_question-' + str(question_number + 1))
    else:
        builder.button(text='Завершить викторину', callback_data='quiz_end')


    if right_answer == user_answer:
        temp = f'🥳 Ответ правильный! Вы получаете один балл!'
        data = await state.get_data()
        await state.update_data(right_answers = data.get('right_answers') + 1)
    else:
        temp = f'😔 Ответ неверный! Правильным ответом был вариант: {right_answer}'
    await callback.message.answer_photo(photo=quiz_answers[question_number].get('photo'), caption=temp, reply_markup=builder.as_markup())


@router.callback_query(Quiz.QS, F.data.startswith('next_question'))
async def next_question(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await callback.answer()
    question_number = int(callback.data.split('-')[1])

    builder = InlineKeyboardBuilder()
    for answer in quiz_answers[question_number].get('answer'):
        builder.button(text=answer, callback_data=f'Quiz-{question_number}-_' + answer)
    builder.adjust(5)

    await callback.message.answer(text=quiz_answers[question_number].get('question'), reply_markup=builder.as_markup())

@router.callback_query(Quiz.QS, F.data == 'quiz_end')
async def quiz_end(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await callback.answer()
    data = await state.get_data()
    r_answers = data.get('right_answers')
    procent = round((r_answers / len(quiz_answers)) * 100)
    builder = InlineKeyboardBuilder()
    builder.button(text='Меню 📝', callback_data='help')
    await callback.message.answer(text=f'🎉 Вы завершили викторину! 🎊\n\n📊 Вы ответили правильно на {r_answers} из {len(quiz_answers)}!\n\n😎 Процент: {procent}%', reply_markup=kb)