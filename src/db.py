from typing import Type

from aiogram.contrib.fsm_storage.mongo import MongoStorage

from beanie import init_beanie
from beanie.odm.documents import DocType

from src import config

storage: MongoStorage = MongoStorage(uri=config.MONGODB_URI, db_name=config.DB_NAME)


async def init_db() -> None:
    await init_beanie(database=await storage.get_db(), document_models=[
        "src.exercises.model.Exercise",
        "src.workout_programs.model.WorkoutWeekProgram",
        "test.test_search.TestItemModel",
    ])

