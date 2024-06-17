from aiogram.fsm.state import StatesGroup, State


class CreateEventState(StatesGroup):
    photo = State()
    title = State()
    description = State()
    event_date = State()
    link = State()