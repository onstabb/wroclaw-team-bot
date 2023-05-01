__all__ = ("bot", "dp", )

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode

from config import BOT_TOKEN
from db import storage


bot: Bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
dp: Dispatcher = Dispatcher(bot=bot, storage=storage)





