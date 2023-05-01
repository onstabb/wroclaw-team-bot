import asyncio
import logging
from pprint import pprint

from aiogram.types import BotCommand
from aiogram.dispatcher import Dispatcher

from src.entry.handlers import dp
from src.admin.handlers import dp
from src.exercises.handlers import dp
from src.workout_programs.handlers import dp

from src.db import init_db


logging.basicConfig(level=logging.DEBUG)
logger: logging.Logger = logging.getLogger(__name__)


async def set_commands():
    commands: list = [
        BotCommand(command="/start", description="Main menu"),
        BotCommand(command="/admin", description="Admin panel"),

    ]
    await dp.bot.set_my_commands(commands=commands)


async def on_start(_dispatcher: Dispatcher) -> None:
    await init_db()

    await set_commands()


def main():
    from aiogram import executor
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_start,)


if __name__ == '__main__':
    main()

