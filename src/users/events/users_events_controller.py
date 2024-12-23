import os

from aiogram.types import Message, InlineKeyboardMarkup, InputMediaPhoto, FSInputFile, InlineKeyboardButton

from src.users.events.users_events_service import UsersEventsService
from src.users.keyboards.inline.users_inline_keyboards import UsersInlineKeyboards
from src.users.keyboards.reply.users_reply_keyboards import UsersReplyKeyboards
from utils.lexicon.load_lexicon import load_lexicon
from utils.pagen.pagen_builder import PagenBuilder


class UsersEventsController:
    def __init__(self):
        self.pagen_builder: PagenBuilder = PagenBuilder()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

        self.users_inline_keyboards: UsersInlineKeyboards = UsersInlineKeyboards()
        self.users_reply_keyboards: UsersReplyKeyboards = UsersReplyKeyboards()

        self.users_service: UsersEventsService = UsersEventsService()

    async def users_get_active_events(self, msg: Message) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # png = FSInputFile(os.path.join(current_dir, '..', '..', 'static', 'events', 'temp_png.png'))
        png = FSInputFile(os.path.join(current_dir, '..', '..', 'static', 'events', '1.jpg'))

        await msg.answer_photo(photo=png,
                               caption='Не упусти Событие – стань его частью',
                               reply_markup=InlineKeyboardMarkup(
                                   inline_keyboard=[
                                       [InlineKeyboardButton(text='Календарь событий',
                                                             url='https://mol-rm.ru/events/main/')],
                                       [InlineKeyboardButton(text='Следить за событиями в сообществе ВКонтакте',
                                                             url='https://vk.com/mol13rus/')],
                                       [InlineKeyboardButton(text='Следить за событиями в сообществе в Телеграм-канале',
                                                             url='https://t.me/mol13rus/')],
                                   ]
                               ))

    # async def users_get_active_events(self, msg: Message, offset=0, edit=False) -> None:
        # try:
        #     events = await self.users_service.get_active_events(offset=offset)
        #     events_count = await self.users_service.get_active_events_count()
        #
        #     pages = events_count[0][0]
        #
        #     pagen_callback_data = f"_events-{offset}"
        #
        #     if pages > 0:
        #         pagen = await self.pagen_builder.build_users_pagen(
        #             pages=pages,
        #             offset=offset,
        #             callback_data=pagen_callback_data
        #         )
        #
        #         button = await self.users_inline_keyboards.users_events_entity_keyboard(url=events[0][4])
        #
        #         inline_keyboard = InlineKeyboardMarkup(
        #             inline_keyboard=[
        #                 pagen,
        #                 button
        #             ]
        #         )
        #
        #         photo = events[0][0]
        #
        #         msg_text = f"{offset + 1} из {pages}\n\n" \
        #                    f"<b>{events[0][1]}</b>\n\n" \
        #                    f"{events[0][2]}\n\n" \
        #                    f"<i><u>{events[0][3]}</u></i>"
        #
        #         if edit:
        #             media = InputMediaPhoto(media=photo, caption=msg_text, parse_mode="HTML")
        #             await msg.edit_media(media=media, reply_markup=inline_keyboard)
        #         else:
        #             keyboard = await self.users_reply_keyboards.users_events_panel_keyboard()
        #
        #             await msg.answer_photo(photo=photo,
        #                                    caption=msg_text,
        #                                    reply_markup=inline_keyboard,
        #                                    parse_mode="HTML")
        #
        #             await msg.answer(self.replicas['users']['other']['option'],
        #                              reply_markup=keyboard)
        #     else:
        #         back_to_main_menu_btn = await (self.users_inline_keyboards.
        #                                        users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))
        #
        #         await msg.answer(self.replicas['users']['other']['empty'],
        #                          reply_markup=back_to_main_menu_btn)
        #
        # except Exception as e:
        #     print(f"Error while getting events by user: {e}")
        #
        #     back_to_main_menu_btn = await (self.users_inline_keyboards.
        #                                    users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))
        #
        #     await msg.answer(self.replicas['general']['error'],
        #                      reply_markup=back_to_main_menu_btn)

    async def users_get_calendar_events(self, msg: Message) -> None:
        keyboard = await self.users_inline_keyboards.users_redirect_calendar_events()
        main_menu_keyboard = await self.users_reply_keyboards.main_users_to_menu_panel_keyboard()

        await msg.answer(self.replicas['users']['other']['redirect'],
                         reply_markup=keyboard)

        await msg.answer(self.replicas['users']['other']['option'],
                         reply_markup=main_menu_keyboard)
