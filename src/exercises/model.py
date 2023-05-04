import logging
from typing import Any

from beanie import Document, Indexed
from beanie.odm.operators.find.evaluation import RegEx
from pydantic import Field, BaseModel, validator

from src.exercises.helpers import prepare_text

logger: logging.Logger = logging.getLogger(__name__)


class Exercise(Document):
    title: str
    keyname: Indexed(str, unique=True) = ""
    tg_file_ref: Indexed(str, unique=True)
    description: str = ""

    @validator("keyname", always=True)
    def set_keyname(cls, keyname: str, values: dict[str, Any]) -> str:
        if not keyname:
            keyname = prepare_text(values["title"])
            return keyname
        return keyname

    class Settings:
        name: str = "exercises"


async def get_count() -> int:
    return await Exercise.count()


async def search_exercise(query: str) -> list[Exercise]:
    query = prepare_text(query)
    exercises: list[Exercise] = await Exercise.find(RegEx(Exercise.keyname, f"^{query}")).to_list()

    for exercise in exercises:
        if query == exercise.name:
            return [exercise]

    return exercises


async def update_exercise(exercise: Exercise) -> None:
    await exercise.save()


async def create_exercise(exercise: Exercise) -> None:
    await exercise.create()


# async def del_exercise(name: str) -> None:
#     await Exercise.find_one(Exercise.name == name.lower()).delete()
