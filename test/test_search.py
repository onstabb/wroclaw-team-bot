import asyncio
from datetime import date, timedelta

from beanie import Document, Indexed
from beanie.odm.operators.find.evaluation import Text
from pymongo import TEXT

from src.db import init_db


class TestItemModel(Document):
    name: Indexed(str, unique=True, index_type=TEXT)

    class Settings:
        name = "test_item_model"


async def main(argv=()):
    await init_db()

    names = ["Waga leżąc", "Drabinka brzuch", "Pająk", "X-men", "Brzęk", "Waga Podpinać", "Waga bój", "Waga"]

    for name in names:
        exercise = TestItemModel(name=name)
        await exercise.create()

    products = await TestItemModel.find(Text("waga")).to_list()
    print(products)


if __name__ == '__main__':
    asyncio.run(main())
