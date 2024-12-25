import os

from aiogram.types import Message, FSInputFile

from src.users.keyboards.inline.users_inline_keyboards import UsersInlineKeyboards
from src.users.keyboards.reply.users_reply_keyboards import UsersReplyKeyboards
from utils.lexicon.load_lexicon import load_lexicon


class UsersReservationController:
    def __init__(self):
        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

        self.users_inline_keyboards: UsersInlineKeyboards = UsersInlineKeyboards()
        self.users_reply_keyboards: UsersReplyKeyboards = UsersReplyKeyboards()

    async def users_reservation_redirect(self, msg: Message) -> None:
        keyboard = await self.users_inline_keyboards.users_redirect_to_reservation_keyboard()
        main_menu_keyboard = await self.users_reply_keyboards.main_users_to_menu_panel_keyboard()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        photo = FSInputFile(os.path.join(current_dir, '..', '..', 'static', 'reservation', '1.jpeg'))

        await msg.answer_photo(photo=photo,
                               caption=self.replicas['users']['reservation'],
                               reply_markup=keyboard)

        await msg.answer(self.replicas['users']['other']['option'],
                         reply_markup=main_menu_keyboard)
