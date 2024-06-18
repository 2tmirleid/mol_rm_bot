from aiogram.types import Message

from src.users.keyboards.reply.users_reply_keyboards import UsersReplyKeyboards
from utils.lexicon.load_lexicon import load_lexicon


class MainUsersController:
    def __init__(self):
        self.lexicon = load_lexicon()
        self.buttons = self.lexicon.get("buttons")
        self.callback_data = self.lexicon.get("callback_data")
        self.greetings = self.lexicon.get("greetings")
        self.replicas = self.lexicon.get("replicas")

        self.users_reply_keyboards: UsersReplyKeyboards = UsersReplyKeyboards()

    async def users_get_started(self, msg: Message) -> None:
        keyboard = await self.users_reply_keyboards.main_users_to_menu_panel_keyboard()

        await msg.answer(self.greetings['user'],
                         reply_markup=keyboard)

    async def get_main_users_main_menu_panel(self, msg: Message) -> None:
        keyboard = await self.users_reply_keyboards.main_users_menu_panel_keyboard()

        await msg.answer(self.replicas['users']['other']['option'],
                         reply_markup=keyboard)
