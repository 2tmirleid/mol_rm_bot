from aiogram.types import Message, InlineKeyboardMarkup, InputMediaPhoto, InlineKeyboardButton

from src.users.contacts.users_contacts_service import UsersContactsService
from src.users.keyboards.inline.users_inline_keyboards import UsersInlineKeyboards
from src.users.keyboards.reply.users_reply_keyboards import UsersReplyKeyboards
from utils.lexicon.load_lexicon import load_lexicon
from utils.pagen.pagen_builder import PagenBuilder


class UsersContactsController:
    def __init__(self):
        self.pagen_builder: PagenBuilder = PagenBuilder()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

        self.users_inline_keyboards: UsersInlineKeyboards = UsersInlineKeyboards()
        self.users_reply_keyboards: UsersReplyKeyboards = UsersReplyKeyboards()

        self.users_service: UsersContactsService = UsersContactsService()

    async def users_get_contacts(self, msg: Message) -> None:
        contacts_url_inline_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Контакты команды #МолодёжьМордовии',
                                      url='https://google.com/')]
            ]
        )

        await msg.answer(self.replicas['users']['other']['redirect'],
                         reply_markup=contacts_url_inline_keyboard)

    # async def users_get_contacts(self, msg: Message, offset=0, edit=False) -> None:
    #     try:
    #         back_to_main_menu_btn = await (self.users_inline_keyboards.
    #                                        users_dynamic_entity_to_main_menu_panel_keyboard())
    #
    #         contacts = await self.users_service.get_contacts(offset=offset)
    #         contacts_count = await self.users_service.get_contacts_count()
    #
    #         pages = contacts_count[0][0]
    #
    #         pagen_callback_data = f"_contacts-{offset}"
    #
    #         if pages > 0:
    #             pagen = await self.pagen_builder.build_users_pagen(
    #                 pages=pages,
    #                 offset=offset,
    #                 callback_data=pagen_callback_data
    #             )
    #
    #             button = await self.users_inline_keyboards.users_contacts_entity_keyboard(phone=contacts[0][3])
    #
    #             inline_keyboard = InlineKeyboardMarkup(
    #                 inline_keyboard=[
    #                     pagen,
    #                     button
    #                 ]
    #             )
    #
    #             photo = contacts[0][0]
    #
    #             msg_text = f"{offset + 1} из {pages}\n\n" \
    #                        f"<b>{contacts[0][1]}</b>\n\n" \
    #                        f"{contacts[0][2]}\n\n"
    #
    #             if edit:
    #                 if photo:
    #                     media = InputMediaPhoto(media=photo, caption=msg_text, parse_mode="HTML")
    #                     await msg.edit_media(media=media, reply_markup=inline_keyboard)
    #                 else:
    #                     await msg.edit_text(text=msg_text, reply_markup=inline_keyboard, parse_mode="HTML")
    #             else:
    #                 keyboard = await self.users_reply_keyboards.users_contacts_panel_keyboard()
    #
    #                 if photo:
    #                     await msg.answer_photo(photo=photo,
    #                                            caption=msg_text,
    #                                            reply_markup=inline_keyboard,
    #                                            parse_mode="HTML")
    #                 else:
    #                     await msg.answer(text=msg_text, reply_markup=inline_keyboard, parse_mode="HTML")
    #
    #                 await msg.answer(self.replicas['users']['other']['option'],
    #                                  reply_markup=keyboard)
    #         else:
    #             back_to_main_menu_btn = await (self.users_inline_keyboards.
    #                                            users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))
    #
    #             await msg.answer(self.replicas['users']['other']['empty'],
    #                              reply_markup=back_to_main_menu_btn)
    #
    #     except Exception as e:
    #         print(f"Error while getting contacts by user: {e}")
    #
    #         back_to_main_menu_btn = await (self.users_inline_keyboards.
    #                                        users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))
    #
    #         await msg.answer(self.replicas['general']['error'],
    #                          reply_markup=back_to_main_menu_btn)

    async def users_get_contacts_phone(self, msg: Message, phone: str) -> None:
        await msg.answer(f"{phone}")

    async def users_ask_question(self, msg: Message) -> None:
        keyboard = await self.users_inline_keyboards.users_redirect_ask_question()
        main_menu_keyboard = await self.users_reply_keyboards.main_users_to_menu_panel_keyboard()

        await msg.answer(self.replicas['users']['other']['redirect'],
                         reply_markup=keyboard)

        await msg.answer(self.replicas['users']['other']['option'],
                         reply_markup=main_menu_keyboard)