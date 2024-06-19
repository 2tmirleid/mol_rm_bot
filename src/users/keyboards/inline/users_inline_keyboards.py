from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.lexicon.load_lexicon import load_lexicon


class UsersInlineKeyboards:
    def __init__(self):
        self.lexicon = load_lexicon()
        self.buttons = self.lexicon.get("buttons")
        self.callback_data = self.lexicon.get("callback_data")

    async def users_redirect_to_reservation_keyboard(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=self.buttons['users']['reservation']['redirect'],
                                      url=self.callback_data['users']['url']['reservation']['redirect'])]
            ]
        )
