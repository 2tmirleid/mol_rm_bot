from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.states.example_state import ExampleState

router: Router = Router()

example_state: ExampleState = ExampleState()


@router.message(StateFilter(example_state.example), F.text)
async def example_fsm(msg: Message, state: FSMContext):
    ...
