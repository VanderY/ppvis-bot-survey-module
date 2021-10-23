from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import config


class MenuStates(StatesGroup):
    professor = State()


async def prof_menu(message: types.Message, state: FSMContext):
    await MenuStates.professor.set()

    await message.answer("Преподское меню")


def register_handlers_survey(dp: Dispatcher):
    dp.register_message_handler(prof_menu, state=MenuStates.professor)
