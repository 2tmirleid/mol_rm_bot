from aiogram.types import Message

from src.users.keyboards.inline.users_inline_keyboards import UsersInlineKeyboards
from utils.lexicon.load_lexicon import load_lexicon


class UsersReservationController:
    def __init__(self):
        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

        self.users_inline_keyboards: UsersInlineKeyboards = UsersInlineKeyboards()

    async def users_reservation_redirect(self, msg: Message) -> None:
        keyboard = await self.users_inline_keyboards.users_redirect_to_reservation_keyboard()

        await msg.answer(self.replicas['users']['other']['redirect'],
                         reply_markup=keyboard)
