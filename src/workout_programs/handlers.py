from aiogram import types
from aiogram.utils.markdown import hbold

from src import dateutils
from src.loader import dp
from src.keys import TextKeys
from src.i18n import _
from src.workout_programs import model


@dp.message_handler(text_key=TextKeys.GET_PROGRAM, state="*")
async def get_actual_program(message: types.Message):

    program: model.WorkoutWeekProgram | None = await model.get_program_by_week(dateutils.get_now())

    if not program:
        await message.answer(_("error_no_actual_workout_week_program_exists"))
        return

    media: types.MediaGroup = types.MediaGroup()

    caption: str = hbold(_("workout_program_is_actual")) + "✅\n\n" + program.description

    for file_ref in program.file_refs:
        if caption:
            media.attach_photo(file_ref, caption=caption)
            caption = ""
            continue

        media.attach_photo(file_ref)

    await message.answer_media_group(media, )

