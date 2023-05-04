__all__ = ("bot", "dp", )

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode

from src.config import BOT_TOKEN, PROXY_URL
from src.db import storage


bot: Bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML, proxy=PROXY_URL)
dp: Dispatcher = Dispatcher(bot=bot, storage=storage)





