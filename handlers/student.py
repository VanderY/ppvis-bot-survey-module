from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config
import keyboards
import spreadsheets
from handlers.common import GeneralStates


class StudentStates(StatesGroup):
    passes_survey = State()


async def menu(message: types.Message, state: FSMContext):
    await message.answer("Студент")


async def survey(message: types.Message, state: FSMContext):
    await StudentStates.passes_survey.set()
    await state.update_data(survey=spreadsheets.get_test())
    await state.update_data(answers={})
    kb = keyboards.start_survey_keyboard()
    await message.answer("Список команд:", reply_markup=kb)


def register_handlers_student(dp: Dispatcher):
    dp.register_message_handler(survey, commands=['survey'], state=GeneralStates.student)
    dp.register_message_handler(menu, commands=['menu'], state=GeneralStates.student)
