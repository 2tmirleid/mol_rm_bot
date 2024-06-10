from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.lexicon.load_lexicon import load_lexicon


class AdminsReplyKeyboards:
    def __init__(self):
        self.lexicon = load_lexicon()

    def main_admins_to_menu_panel_keyboard(self) -> ReplyKeyboardMarkup:
        buttons = self.lexicon.get("buttons")

        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=f"{buttons["admin"]["other"]["to_main_panel"]}")
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    def main_admins_menu_panel_keyboard(self) -> ReplyKeyboardMarkup:
        buttons = self.lexicon.get("buttons")

        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=f"{buttons["admin"]["main_panel"]["programs"]}"),
                    KeyboardButton(text=f"{buttons["admin"]["main_panel"]["events"]}")
                ],
                [
                    KeyboardButton(text=f"{buttons["admin"]["main_panel"]["vacancies"]}"),
                    KeyboardButton(text=f"{buttons["admin"]["main_panel"]["admins"]}")
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
