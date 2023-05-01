from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminPanel(StatesGroup):
    main: State = State()
    add_current_week_program: State = State()
    add_next_week_program: State = State()
    add_individual_program: State = State()
    add_exercise: State = State()
    update_exercise: State = State()

