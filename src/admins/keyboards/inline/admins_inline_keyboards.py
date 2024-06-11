from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.lexicon.load_lexicon import load_lexicon


class AdminsInlineKeyboards:
    def __init__(self):
        self.lexicon = load_lexicon()
        self.buttons = self.lexicon.get("buttons")
        self.callback_data = self.lexicon.get("callback_data")

    async def admins_dynamic_entity_keyboard(self, callback_data: str) -> list:
        add_btn_text = self.buttons['admin']['general']['add']
        edit_btn_text = self.buttons['admin']['general']['edit']
        delete_btn_text = self.buttons['admin']['general']['delete']

        add_btn_clb_data = self.callback_data['admin']['general']['add'] + callback_data.rsplit("-", 1)[0]
        edit_btn_clb_data = self.callback_data['admin']['general']['edit'] + callback_data
        delete_btn_clb_data = self.callback_data['admin']['general']['delete'] + callback_data

        return [
                InlineKeyboardButton(text=add_btn_text, callback_data=add_btn_clb_data),
                InlineKeyboardButton(text=edit_btn_text, callback_data=edit_btn_clb_data),
                InlineKeyboardButton(text=delete_btn_text, callback_data=delete_btn_clb_data)
        ]

    async def admins_dynamic_create_entity_keyboard(self, callback_data: str) -> list:
        add_btn_text = self.buttons['admin']['general']['add']
        add_btn_clb_data = self.callback_data['admin']['general']['add'] + callback_data

        return [
            InlineKeyboardButton(text=add_btn_text, callback_data=add_btn_clb_data)
        ]
