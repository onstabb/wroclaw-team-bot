import asyncio
from datetime import date, timedelta

from src.db import init_db
from src.dateutils import get_now
from src.workout_programs import model


async def main(argv=()):
    await init_db()

    program = await model.get_program_by_week(key_date=get_now())
    print(program)


if __name__ == '__main__':
    asyncio.run(main())