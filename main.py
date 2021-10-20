import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import keyboards
import spreadsheets
from StateMachine import StateMachine
import config
from aiogram import Bot, Dispatcher, executor, types

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
logger.warning("Starting bot")
bot = Bot(token=config.TG_API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.callback_query_handler(lambda c: c.data, state=StateMachine.ANSWERING_TEST)
async def callback_answering_test(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.message.chat.id)
    separated_data = callback_query.data.split(";")
    question_number = int(separated_data[1])
    survey = (await state.get_data())['survey']
    if len(separated_data) > 2:
        current_question = survey[question_number - 1]
        answers = (await state.get_data())['answers']
        answers[f"Question {question_number - 1}"] = {
            "Вопрос": str(survey[question_number - 1]['Вопрос']),
            f"{separated_data[2]}": f"{current_question[f'{separated_data[2]}']}"
        }
        await state.update_data(answers=answers)
    if question_number < len(survey):
        current_question = survey[question_number]
        answers_kb = keyboards.get_answers_keyboard(current_question, question_number)
        await bot.edit_message_text(text=f"{current_question['Вопрос']}", reply_markup=answers_kb,
                                    chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id)
        await bot.answer_callback_query(callback_query.id)
    else:
        answers = (await state.get_data())['answers']
        print(answers)
        await state.reset_state()
        await bot.edit_message_text(text=f"Вы прошли тест",
                                    chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id)
        await bot.answer_callback_query(callback_query.id)


@dp.message_handler(commands=['test'])
async def test_message(message: types.Message):
    state = dp.current_state(user=message.chat.id)
    await state.set_state(StateMachine.all()[0])
    await state.update_data(survey=spreadsheets.get_test())
    await state.update_data(answers={})
    answers_kb = InlineKeyboardMarkup(row_width=2)
    start_btn = InlineKeyboardButton(f"Начать тест", callback_data=f"start;0")
    answers_kb.add(start_btn)
    await message.answer("Список команд:", reply_markup=answers_kb)


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await message.answer("Список команд:")


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer("Привет!")


if __name__ == '__main__':
    executor.start_polling(dp)
