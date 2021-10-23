from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.helper import Helper, HelperMode, ListItem


class StateMachine(StatesGroup):
    answering_test = State()


