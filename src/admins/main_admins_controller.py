from aiogram.types import Message

from src.admins.keyboards.reply.admins_reply_keyboards import AdminsReplyKeyboards
from utils.lexicon.load_lexicon import load_lexicon


class MainAdminsController:
    def __init__(self):
        self.admins_reply_keyboards: AdminsReplyKeyboards = AdminsReplyKeyboards()

        self.lexicon = load_lexicon()
        self.greeting = self.lexicon.get("greetings")
        self.replicas = self.lexicon.get("replicas")

    async def admins_get_started(self, msg: Message) -> None:
        await msg.answer(f"{self.greeting['admin']}",
                         reply_markup=self.admins_reply_keyboards.main_admins_to_menu_panel_keyboard())

    async def get_main_admins_main_menu_panel(self, msg: Message) -> None:
        await msg.answer(f"{self.replicas['admin']['other']['option']}",
                         reply_markup=self.admins_reply_keyboards.main_admins_menu_panel_keyboard())
