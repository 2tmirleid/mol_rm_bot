import os

from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton

from src.users.keyboards.inline.users_inline_keyboards import UsersInlineKeyboards
from src.users.keyboards.reply.users_reply_keyboards import UsersReplyKeyboards
from utils.lexicon.load_lexicon import load_lexicon


class UsersSupportController:
    def __init__(self):
        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

        self.users_inline_keyboards: UsersInlineKeyboards = UsersInlineKeyboards()
        self.users_reply_keyboards: UsersReplyKeyboards = UsersReplyKeyboards()

    async def users_get_support_menu(self, msg: Message) -> None:
        keyboard = await self.users_reply_keyboards.users_support_menu()

        await msg.answer(self.replicas['users']['other']['option'],
                         reply_markup=keyboard)

    async def users_get_team_info(self, msg: Message) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))

        pdf = FSInputFile(os.path.join(current_dir, '..', '..', 'static', 'team', 'temp_pdf.pdf'))

        await msg.answer_document(pdf,
                                  reply_markup=await self.users_inline_keyboards.users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

    async def users_get_contacts_info(self, msg: Message) -> None:
        contacts_url_inline_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Контакты команды #МолодёжьМордовии',
                                      url='https://google.com/')]
            ]
        )

        await msg.answer(self.replicas['users']['other']['redirect'],
                         reply_markup=contacts_url_inline_keyboard)

    async def users_get_part_info(self, msg: Message) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))

        pdf = FSInputFile(os.path.join(current_dir, '..', '..', 'static', 'part', 'temp_pdf.pdf'))

        await msg.answer_document(pdf,
                                  reply_markup=await self.users_inline_keyboards.users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

    async def users_get_schedule_info(self, msg: Message) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))

        png = FSInputFile(os.path.join(current_dir, '..', '..', 'static', 'schedule', 'temp_png.png'))

        await msg.answer_photo(png,
                                  reply_markup=await self.users_inline_keyboards.users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

    async def users_get_places_info(self, msg: Message) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))

        pdf = FSInputFile(os.path.join(current_dir, '..', '..', 'static', 'schedule', 'temp_pdf.pdf'))

        await msg.answer_document(pdf,
                               reply_markup=await self.users_inline_keyboards.users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

    async def users_get_rules_info(self, msg: Message) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))

        pdf = FSInputFile(os.path.join(current_dir, '..', '..', 'static', 'rules', 'temp_pdf.pdf'))

        await msg.answer_document(pdf,
                                  reply_markup=await self.users_inline_keyboards.users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))