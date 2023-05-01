from aiogram.dispatcher.filters.state import StatesGroup, State


class FindExercise(StatesGroup):
    input_name: State = State()
