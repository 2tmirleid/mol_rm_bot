from aiogram.types import Message

from utils.lexicon.load_lexicon import load_lexicon


class AdminsCommandsController:
    def __init__(self):
        ...

    async def get_main_admin_panel(self, msg: Message) -> None:
        lexicon = await load_lexicon()
        greeting = lexicon.get("greetings")

        await msg.answer(f"{greeting["admin"]}")
