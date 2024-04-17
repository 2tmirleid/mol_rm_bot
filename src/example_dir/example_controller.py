from aiogram.types import Message


# from src.example_dir.example_service import ExampleService


class ExampleController:
    def __init__(self):
        ...
        # self.example_service: ExampleService = ExampleService()

    async def example_func(self, msg: Message):
        await msg.answer("example_msg")
