from aiogram.fsm.state import StatesGroup, State


class CreateProgramState(StatesGroup):
    photo = State()
    title = State()
    description = State()
    link = State()
