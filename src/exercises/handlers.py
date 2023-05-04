from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold

from src.loader import dp
from src.exercises import model
from src.exercises.helpers import prepare_text
from src.exercises.states import FindExercise
from src.i18n import _
from src.keys import TextKeys, TextKeyBuilder


MAX_SEARCH_QUERY_RESULT: int = 3


@dp.message_handler(text_key=TextKeys.FIND_EXERCISE, state="*")
async def input_exercise_name(message: types.Message, state: FSMContext) -> None:
    markup: types.ReplyKeyboardMarkup = TextKeyBuilder(
        resize_keyboard=True, is_persistent=True, input_field_placeholder=_("input_exercise_name_placeholder")
    )

    markup.add(TextKeys.MAIN_MENU("↩️"))
    await message.answer(
        _("exercises_input_name_message") + "\n" +
        _("exercises_count {count}").format(count=await model.get_count()),
        reply_markup=markup
    )
    await state.set_state(FindExercise.input_name.state)


@dp.message_handler(state=FindExercise.input_name.state)
async def find_exercise(message: types.Message) -> None:
    exercise_name: str = message.text
    exercises: list[model.Exercise] = await model.search_exercise(exercise_name)

    markup: types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_key: str = str(TextKeys.MAIN_MENU("↩️"))

    if not exercises:
        await message.answer(_("error_exercise_not_found"))
        return

    if len(exercises) > 1:

        for exercise in exercises[:MAX_SEARCH_QUERY_RESULT]:
            markup.add(exercise.title)

        markup.add(main_menu_key)
        await message.answer(_("exercises_multiple_result_search_query"), reply_markup=markup)
        return

    markup.add(main_menu_key)
    await message.answer_video(
        video=exercises[0].tg_file_ref,
        caption=f"{hbold(exercises[0].title)}\n{exercises[0].description}",
        reply_markup=markup
    )


