from aiogram import types
from aiogram.dispatcher.filters import Filter

from src.model import is_admin


class BotAdminFilter(Filter):
    key: str = "bot_admin_only"

    async def check(self, message: types.Message) -> bool:
        return await is_admin(message.from_user.id)
