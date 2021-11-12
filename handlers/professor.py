import json

import gspread.exceptions
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config
import keyboards
import spreadsheets
from handlers.common import GeneralStates


class ProfessorStates(StatesGroup):
    sheet_name_waiting = State()
    checking_survey = State()
    start_survey = State()


async def menu(message: types.Message, state: FSMContext):
    kb = keyboards.get_professor_keyboard()
    await message.answer("Меню", reply_markup=kb)


async def sheet_name_message(callback_query: types.CallbackQuery, state: FSMContext):
    kb = keyboards.get_tests_keyboard()
    await callback_query.message.answer(text="Список доступных тестов", reply_markup=kb)
    if callback_query.data.startswith("check"):
        await ProfessorStates.checking_survey.set()
    elif callback_query.data.startswith("start"):
        await ProfessorStates.start_survey.set()
    else:
        await callback_query.message.edit_text("Произошла непредвиденная ошибка :(")
    await callback_query.answer()


async def check_survey(message: types.Message, state: FSMContext):
    kb = keyboards.get_professor_keyboard()
    try:
        survey = spreadsheets.get_test(message.text)
        question_number = 0
        for question in survey:
            answers_kb = keyboards.get_answers_keyboard(question, question_number)
            question_number += 1
            await message.bot.send_message(chat_id=message.chat.id,
                                           text=f"{question['Вопрос']}",
                                           reply_markup=answers_kb)
        await message.answer(f"Выведено {question_number} вопросов", reply_markup=kb)
        await GeneralStates.professor.set()
    except gspread.exceptions.WorksheetNotFound:
        await message.answer(f"Лист с названием {message.text} не найден :(")
        await message.answer("Меню", reply_markup=kb)
        await GeneralStates.professor.set()


async def start_survey(message: types.Message, state: FSMContext):
    kb = keyboards.get_professor_keyboard()
    start_survey_kb = keyboards.start_survey_keyboard()
    try:
        survey = spreadsheets.get_test(message.text)
        with open(f'{message.text}.json', 'w', encoding='utf-8') as f:
            json.dump(survey, f, ensure_ascii=False, indent=4)
        student_count = 0
        for student in config.STUDENTS_ID:
            await message.bot.send_message(text="Доступен новый тест.\n"
                                                "Чтобы приступить, нажмите кнопку ниже",
                                           reply_markup=start_survey_kb,
                                           chat_id=student)
            student_count += 1
        await message.answer(f"Сообщение выведено {student_count} студентам")
        await message.answer("Меню", reply_markup=kb)
        await GeneralStates.professor.set()
    except gspread.exceptions.WorksheetNotFound:
        await message.answer(f"Лист с названием {message.text} не найден :(")
        await message.answer("Меню", reply_markup=kb)
        await GeneralStates.professor.set()


async def handle_test_name(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer("rjkj,jr gjdtcbkcz")


def register_handlers_professor(dp: Dispatcher):
    # dp.register_message_handler(survey, commands=['menu'], state=GeneralStates.professor)
    dp.register_message_handler(menu, commands=['menu'], state=GeneralStates.professor)
    dp.register_callback_query_handler(handle_test_name, lambda c: c.data.startswith("test"),
                                       state=ProfessorStates.checking_survey)
    dp.register_callback_query_handler(sheet_name_message, state=GeneralStates.professor)
    dp.register_message_handler(check_survey, state=ProfessorStates.checking_survey)
    dp.register_message_handler(start_survey, state=ProfessorStates.start_survey)
