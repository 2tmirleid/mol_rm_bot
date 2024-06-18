from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.lexicon.load_lexicon import load_lexicon


class UsersReplyKeyboards:
    def __init__(self):
        self.lexicon = load_lexicon()
        self.buttons = self.lexicon.get("buttons")

    async def main_users_to_menu_panel_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=self.buttons['users']['other']['to_main_panel'])]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    async def main_users_menu_panel_keyboard(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=self.buttons['users']['main_panel']['programs']),
                    KeyboardButton(text=self.buttons['users']['main_panel']['events'])
                ],
                [
                    KeyboardButton(text=self.buttons['users']['main_panel']['vacancies']),
                    KeyboardButton(text=self.buttons['users']['main_panel']['reservation'])
                ],
                [
                    KeyboardButton(text=self.buttons['users']['main_panel']['contacts']),
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
