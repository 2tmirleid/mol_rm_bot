from aiogram.fsm.state import StatesGroup, State


class EditEventState(StatesGroup):
    event_id = State()
    property = State()
    value = State()
