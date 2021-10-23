import json

from aiogram import Dispatcher, types
from aiogram.bot.bot import Bot as bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import config
import keyboards
from StateMachine import StateMachine
from handlers.common import GeneralStates
from handlers.professor import ProfessorStates
from handlers.student import StudentStates


async def callback_answering_test(callback_query: types.CallbackQuery, state: FSMContext):
    # state = dp.current_state(user=callback_query.message.chat.id)

    with open('Тест.json', encoding='utf-8') as json_file:
        survey = json.load(json_file)
        separated_data = callback_query.data.split(";")
        question_number = int(separated_data[1])
        # survey = (await state.get_data())['survey']
        if len(separated_data) > 2:
            current_question = survey[question_number - 1]
            answers = list((await state.get_data())['answers'])
            is_correct = False
            if current_question['правильный'] == separated_data[2]:
                is_correct = True
            answer = {
                "Вопрос": str(survey[question_number - 1]['Вопрос']),
                "is_correct": is_correct
            }
            answers.append(answer)
            await state.update_data(answers=answers)
        if question_number < len(survey):
            current_question = survey[question_number]
            answers_kb = keyboards.get_answers_keyboard(current_question, question_number)
            await callback_query.message.edit_text(text=f"{current_question['Вопрос']}", reply_markup=answers_kb)
            await callback_query.answer()
        else:
            answers = (await state.get_data())['answers']
            correct_answers = 0
            for answer in answers:
                if answer['is_correct']:
                    correct_answers += 1
            print(answers)
            print(f"{correct_answers}/{len(answers)}")
            await state.reset_state()
            await GeneralStates.student.set()
            await callback_query.message.edit_text(text=f"Вы прошли тест на {correct_answers}/{len(answers)}")
            await callback_query.answer()


def register_handlers_survey(dp: Dispatcher):
    dp.register_callback_query_handler(callback_answering_test, lambda c: c.data, state=GeneralStates.student)
    # dp.register_callback_query_handler(check_survey, lambda c: c.data, state=ProfessorStates.checking_survey)
