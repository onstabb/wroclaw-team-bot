from dataclasses import dataclass, field, asdict

from src.bot import bot
from src.db import storage


async def set_admin(chat_id: int) -> None:
    await storage.update_data(user=(await bot.me).username, data={f"{chat_id}": "admin"})


async def is_admin(chat_id: int) -> bool:
    data: dict = await storage.get_data(user=(await bot.me).username)
    if data.get(str(chat_id)) == "admin":
        return True
    return False


async def unset_admin(chat_id: int) -> None:
    ...


@dataclass
class BaseModel:

    def to_dict(self) -> dict:
        return asdict(self)
