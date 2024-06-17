from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.lexicon.load_lexicon import load_lexicon


class AdminsInlineKeyboards:
    def __init__(self):
        self.lexicon = load_lexicon()
        self.buttons = self.lexicon.get("buttons")
        self.callback_data = self.lexicon.get("callback_data")

    async def admins_dynamic_entity_keyboard(self, callback_data: str) -> list:
        add_btn_text = self.buttons['admin']['general']['add']
        edit_btn_text = self.buttons['admin']['general']['edit']['main']
        delete_btn_text = self.buttons['admin']['general']['delete']

        add_btn_clb_data = self.callback_data['admin']['general']['add'] + callback_data.rsplit("-", 1)[0]
        edit_btn_clb_data = self.callback_data['admin']['general']['edit']['main'] + callback_data
        delete_btn_clb_data = self.callback_data['admin']['general']['delete'] + callback_data

        return [
            InlineKeyboardButton(text=add_btn_text, callback_data=add_btn_clb_data),
            InlineKeyboardButton(text=edit_btn_text, callback_data=edit_btn_clb_data),
            InlineKeyboardButton(text=delete_btn_text, callback_data=delete_btn_clb_data)
        ]

    async def admins_dynamic_entity_to_main_menu_panel_keyboard(
            self, markup: bool = False
    ) -> list or InlineKeyboardMarkup:

        back_to_main_menu_btn = self.buttons['admin']['other']['to_main_panel']
        back_to_main_menu_clb_data = self.callback_data['admin']['other']['to_main_panel']

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

    async def admins_dynamic_create_entity_keyboard(self, callback_data: str) -> list:
        add_btn_text = self.buttons['admin']['general']['add']
        add_btn_clb_data = self.callback_data['admin']['general']['add'] + callback_data

        return [
            InlineKeyboardButton(text=add_btn_text, callback_data=add_btn_clb_data)
        ]

    async def admins_dynamic_edit_entity_keyboard(self, callback_data: str, date=False, admins=False) -> list:
        photo_btn_text = self.buttons['admin']['general']['edit']['photo']
        title_btn_text = self.buttons['admin']['general']['edit']['title']
        description_btn_text = self.buttons['admin']['general']['edit']['description']
        link_btn_text = self.buttons['admin']['general']['edit']['link']
        activity_btn_text = self.buttons['admin']['general']['edit']['activity']

        photo_btn_clb_data = self.callback_data['admin']['general']['edit']['photo'] + callback_data
        title_btn_clb_data = self.callback_data['admin']['general']['edit']['title'] + callback_data
        description_clb_data = self.callback_data['admin']['general']['edit']['description'] + callback_data
        link_btn_clb_data = self.callback_data['admin']['general']['edit']['link'] + callback_data
        activity_btn_clb_data = self.callback_data['admin']['general']['edit']['activity'] + callback_data

        if date:
            date_btn_text = self.buttons['admin']['general']['edit']['date']
            date_btn_clb_data = self.callback_data['admin']['general']['edit']['date'] + callback_data

            return [
                [InlineKeyboardButton(text=photo_btn_text, callback_data=photo_btn_clb_data),
                 InlineKeyboardButton(text=description_btn_text, callback_data=description_clb_data),
                 InlineKeyboardButton(text=title_btn_text, callback_data=title_btn_clb_data)],
                [InlineKeyboardButton(text=link_btn_text, callback_data=link_btn_clb_data),
                 InlineKeyboardButton(text=date_btn_text, callback_data=date_btn_clb_data),
                 InlineKeyboardButton(text=activity_btn_text, callback_data=activity_btn_clb_data)],
            ]
        elif admins:
            name_btn_text = self.buttons['admin']['general']['edit']['name']
            name_btn_clb_data = self.callback_data['admin']['general']['edit']['name'] + callback_data

            phone_btn_text = self.buttons['admin']['general']['edit']['phone']
            phone_btn_clb_data = self.callback_data['admin']['general']['edit']['phone'] + callback_data

            return [
                [InlineKeyboardButton(text=photo_btn_text, callback_data=photo_btn_clb_data),
                 InlineKeyboardButton(text=name_btn_text, callback_data=name_btn_clb_data)],
                [InlineKeyboardButton(text=description_btn_text, callback_data=description_clb_data),
                 InlineKeyboardButton(text=phone_btn_text, callback_data=phone_btn_clb_data)]
            ]
        else:
            return [
                [InlineKeyboardButton(text=photo_btn_text, callback_data=photo_btn_clb_data),
                 InlineKeyboardButton(text=description_btn_text, callback_data=description_clb_data),
                 InlineKeyboardButton(text=title_btn_text, callback_data=title_btn_clb_data)],
                [InlineKeyboardButton(text=link_btn_text, callback_data=link_btn_clb_data),
                 InlineKeyboardButton(text=activity_btn_text, callback_data=activity_btn_clb_data)],
            ]
