from aiogram import Router, F
from aiogram.types import Message

from src.example_dir.example_controller import ExampleController

router: Router = Router()

example_controller: ExampleController = ExampleController()


@router.message(F.text == "example")
async def example(msg: Message):
    await example_controller.example_func(msg)