import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

import keyboards
import spreadsheets
from StateMachine import StateMachine
import config
from aiogram import Bot, Dispatcher, executor, types

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from handlers.common import register_handlers_common
from handlers.professor import register_handlers_professor
from handlers.student import register_handlers_student
from handlers.survey import register_handlers_survey

logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
logger.warning("Starting bot")
bot = Bot(token=config.TG_API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


async def set_commands(tg_bot: Bot):
    commands = [
        BotCommand(command="/test", description="Вывести тест")
    ]
    await tg_bot.set_my_commands(commands)


if __name__ == '__main__':
    register_handlers_survey(dp)
    register_handlers_common(dp)
    register_handlers_student(dp)
    register_handlers_professor(dp)
    # await set_commands(bot)
    executor.start_polling(dp)
