from aiogram.fsm.state import StatesGroup, State


class EditAdminState(StatesGroup):
    admin_id = State()
    property = State()
    value = State()
