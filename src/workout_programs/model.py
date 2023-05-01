from datetime import datetime

from beanie import Document, before_event, Insert, Indexed
from pydantic import Field

from src.dateutils import get_week_range, get_now
from src.workout_programs.exceptions import WeekProgramAlreadyExists


class WorkoutWeekProgram(Document):
    file_refs: list[str]
    week_key: Indexed(datetime) = Field(default_factory=get_now)
    description: str = ""

    @before_event(Insert)
    async def week_validate(self):
        if await get_program_by_week(self.week_key):
            raise WeekProgramAlreadyExists

    class Settings:
        name: str = "workout_programs"


async def create(program: WorkoutWeekProgram) -> None:
    await program.create()


async def get_program_by_week(key_date: datetime) -> WorkoutWeekProgram | None:
    start_of_week, end_of_week = get_week_range(key_date)

    return await WorkoutWeekProgram.find_one(
        WorkoutWeekProgram.week_key >= start_of_week,
        WorkoutWeekProgram.week_key <= end_of_week
    )


async def get_count() -> int:
    return await WorkoutWeekProgram.count()


async def get_last_program() -> WorkoutWeekProgram | None:
    program: list[WorkoutWeekProgram] = await WorkoutWeekProgram.find(

    ).sort(-WorkoutWeekProgram.week_key).limit(1).to_list()
    if not program:
        return None
    return program[0]



