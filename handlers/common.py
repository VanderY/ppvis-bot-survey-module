from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import config


class GeneralStates(StatesGroup):
    professor = State()
    student = State()


async def start(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in config.ADMIN_IDS:
        await GeneralStates.professor.set()
        await message.answer("Вы преподаватель")
    else:
        await GeneralStates.student.set()
        await state.update_data(answers={})
        await message.answer("Вы студент")


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state="*")
