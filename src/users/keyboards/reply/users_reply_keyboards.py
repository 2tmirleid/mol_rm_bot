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

    async def users_programs_panel_keyboard(self) -> ReplyKeyboardMarkup:
        useful_btn_text = self.buttons['users']['programs']['useful']
        backward_btn_text = self.buttons['users']['other']['to_main_panel']

        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=useful_btn_text),
                 KeyboardButton(text=backward_btn_text)]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    async def users_vacancies_panel_keyboard(self) -> ReplyKeyboardMarkup:
        take_part_btn_text = self.buttons['users']['vacancies']['take_part']
        partners_btn_text = self.buttons['users']['vacancies']['partners']
        backward_btn_text = self.buttons['users']['other']['to_main_panel']

        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=take_part_btn_text),
                 KeyboardButton(text=partners_btn_text)],
                [KeyboardButton(text=backward_btn_text)]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    async def users_events_panel_keyboard(self) -> ReplyKeyboardMarkup:
        calendar_btn_text = self.buttons['users']['events']['calendar']
        backward_btn_text = self.buttons['users']['other']['to_main_panel']

        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=calendar_btn_text),
                 KeyboardButton(text=backward_btn_text)]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
