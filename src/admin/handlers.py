import asyncio
import logging
from datetime import datetime
from typing import Literal

import pytz
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State
from aiogram_media_group import media_group_handler
from pymongo.errors import DuplicateKeyError


from src.admin.states import AdminPanel
from src.dateutils import get_next_week_monday, get_now_main_tz
from src.exercises import model as exercises_model
from src.filters import BotAdminFilter
from src.i18n import _
from src.keys import TextKeys, TextKeyBuilder
from src.loader import dp
from src.model import set_admin
from src.workout_programs import model as workout_program_model
from src.workout_programs import exceptions as workout_program_exceptions

logger: logging.Logger = logging.getLogger("AdminPanel")



@dp.message_handler(BotAdminFilter(), Command("setadmin"), state="*")
async def set_user_admin(message: types.Message):
    _split: list[str] = message.text.split(" ")
    await set_admin(int(_split[-1]))
    await message.answer(_("new_admin_successfully_added"))


@dp.message_handler(BotAdminFilter(), text_key=TextKeys.ADMIN_PANEL, state="*")
@dp.message_handler(Command("admin"), BotAdminFilter(), state="*")
async def admin_entry(message: types.Message, state: FSMContext) -> None:
    markup: TextKeyBuilder = TextKeyBuilder(is_persistent=True, resize_keyboard=True)

    markup.add(TextKeys.ADD_EXERCISE, )
    markup.add(TextKeys.ADD_CURRENT_WEEK_PROGRAM)
    markup.add(TextKeys.ADD_NEXT_WEEK_PROGRAM)
    markup.add(TextKeys.MAIN_MENU("↩️"))

    await message.answer(
        _("admin_panel_main"),
        reply_markup=markup
    )
    await state.set_state(AdminPanel.main.state)


@dp.message_handler(BotAdminFilter(), text_key=TextKeys.ADD_EXERCISE, state=AdminPanel.main.state)
async def entry_add_exercise_form(message: types.Message, state: FSMContext) -> None:
    markup: TextKeyBuilder = TextKeyBuilder(is_persistent=True, resize_keyboard=True)
    markup.add(TextKeys.ADMIN_PANEL("↩️"))
    await message.answer(
        _("entry_add_exercise_form") + "\n" + _("add_exercise_rules"),
        reply_markup=markup
    )
    await state.set_state(AdminPanel.add_exercise.state)


@dp.message_handler(BotAdminFilter(), state=AdminPanel.add_exercise.state, content_types=types.ContentType.VIDEO)
async def add_exercise(message: types.Message) -> None:
    try:
        _split: list[str] = message.caption.split("\n")
        name: str = _split[0]

    except (AttributeError, IndexError):
        await message.answer(
            _("error_incorrect_exercise_input") + "\n" +
            _("add_exercise_rules")
        )
        return

    description: str = ""
    if len(_split) > 1:
        description = _split[1]

    file_ref: str = message.video.file_id

    try:
        await exercises_model.create_exercise(
            exercises_model.Exercise(tg_file_ref=file_ref, title=name, description=description)
        )
    except DuplicateKeyError:
        await message.answer(text=_("exercise_is_already_exists"))
        return

    logger.info("Added new exercise: %s", name)
    await message.answer(_("exercise_successfully_added"))


async def entry_add_workout_program(
        message: types.Message, state: FSMContext, week: Literal["current", "next"] = "current"
) -> None:

    text_out: str = _("admin_panel_entry_add_next_week_program")
    state_switch: State = AdminPanel.add_next_week_program
    date: datetime = get_next_week_monday(get_now_main_tz())

    if week == "current":
        text_out = _("admin_panel_entry_add_current_week_program")
        state_switch = AdminPanel.add_current_week_program
        date = get_now_main_tz()

    program: workout_program_model.WorkoutWeekProgram | None = await workout_program_model.get_program_by_week(
        date.astimezone(pytz.UTC)
    )

    if program:
        await message.answer(_("error_workout_week_program_already_exists"))
        return

    markup: TextKeyBuilder = TextKeyBuilder(is_persistent=True, resize_keyboard=True)
    markup.add(TextKeys.ADMIN_PANEL("↩️"))

    await message.answer(text=text_out + "\n" + _("add_workout_program_rules"), reply_markup=markup)
    await state.set_state(state_switch.state)


@dp.message_handler(BotAdminFilter(), text_key=TextKeys.ADD_CURRENT_WEEK_PROGRAM, state=AdminPanel.main.state)
async def entry_add_current_week_workout_program(message: types.Message, state: FSMContext):
    await entry_add_workout_program(message, state, "current")


@dp.message_handler(BotAdminFilter(), text_key=TextKeys.ADD_NEXT_WEEK_PROGRAM, state=AdminPanel.main.state)
async def entry_add_next_week_workout_program(message: types.Message, state: FSMContext):
    await entry_add_workout_program(message, state, "next")


async def add_workout_program(group: list[types.Message], state: FSMContext, week: Literal["current", "next"]) -> None:

    week_date_key: datetime = get_now_main_tz()
    if week == "next":
        week_date_key = get_next_week_monday(week_date_key)

    program: workout_program_model.WorkoutWeekProgram = workout_program_model.WorkoutWeekProgram(
        file_refs=[], week_key=week_date_key.astimezone(pytz.UTC)
    )
    description: str = ""

    for message in group:
        if message.caption:
            description = description
        program.file_refs.append(message.photo[0].file_id)

    program.description = description

    try:
        await workout_program_model.create(program)
    except workout_program_exceptions.WeekProgramAlreadyExists:
        await group[0].answer(_("error_workout_week_program_already_exists"))
        return

    await group[0].answer(_("workout_program_successfully_added"))
    await asyncio.sleep(1)
    await admin_entry(group[0], state)
    return


@dp.message_handler(BotAdminFilter(), state=AdminPanel.add_current_week_program, content_types=types.ContentType.PHOTO)
@media_group_handler(only_album=False)
async def add_current_week_workout_program(group: [types.Message], state: FSMContext) -> None:
    await add_workout_program(group, state, "current")


@dp.message_handler(BotAdminFilter(), state=AdminPanel.add_next_week_program, content_types=types.ContentType.PHOTO)
@media_group_handler(only_album=False)
async def add_current_week_workout_program(group: [types.Message], state: FSMContext) -> None:
    await add_workout_program(group, state, "next")
