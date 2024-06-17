from aiogram.fsm.state import StatesGroup, State


class EditVacancyState(StatesGroup):
    vacancy_id = State()
    property = State()
    value = State()
