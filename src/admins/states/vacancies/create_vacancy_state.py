from aiogram.fsm.state import StatesGroup, State


class CreateVacancyState(StatesGroup):
    photo = State()
    title = State()
    description = State()
    link = State()
