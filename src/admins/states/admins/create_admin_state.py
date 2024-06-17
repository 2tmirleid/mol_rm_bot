from aiogram.fsm.state import StatesGroup, State


class CreateAdminState(StatesGroup):
    photo = State()
    chat_id = State()
    username = State()
    name = State()
    description = State()
    phone = State()
