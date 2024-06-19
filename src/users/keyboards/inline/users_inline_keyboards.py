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

    async def users_redirect_to_useful_docs(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=self.buttons['users']['programs']['redirect'],
                                      url=self.callback_data['users']['url']['programs']['redirect'])]
            ]
        )

    async def users_redirect_take_part_vacancies(self):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=self.buttons['users']['vacancies']['take_part'],
                                      url=self.callback_data['users']['url']['vacancies']['take_part'])]
            ]
        )

    async def users_redirect_partners_vacancies(self):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=self.buttons['users']['vacancies']['partners'],
                                      url=self.callback_data['users']['url']['vacancies']['partners'])]
            ]
        )

    async def users_redirect_calendar_events(self):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=self.buttons['users']['events']['calendar'],
                                      url=self.callback_data['users']['url']['events']['calendar'])]
            ]
        )

    async def users_dynamic_entity_to_main_menu_panel_keyboard(
            self, markup: bool = False
    ) -> list or InlineKeyboardMarkup:

        back_to_main_menu_btn = self.buttons['users']['other']['to_main_panel']
        back_to_main_menu_clb_data = self.callback_data['users']['other']['to_main_panel']

        if markup:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=back_to_main_menu_btn, callback_data=back_to_main_menu_clb_data)]
                ]
            )
        else:
            return [
                InlineKeyboardButton(text=back_to_main_menu_btn, callback_data=back_to_main_menu_clb_data)
            ]

    async def users_programs_entity_keyboard(self, url: str) -> list:
        btn_text = self.buttons['users']['programs']['take_part']

        return [
            InlineKeyboardButton(text=btn_text, url=url)
        ]

    async def users_vacancies_entity_keyboard(self, url: str) -> list:
        btn_text = self.buttons['users']['vacancies']['respond']

        return [
            InlineKeyboardButton(text=btn_text, url=url)
        ]

    async def users_events_entity_keyboard(self, url: str) -> list:
        btn_text = self.buttons['users']['events']['take_part']

        return [
            InlineKeyboardButton(text=btn_text, url=url)
        ]
