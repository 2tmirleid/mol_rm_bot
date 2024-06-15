from aiogram.types import Message, InlineKeyboardMarkup, InputMediaPhoto

from src.admins.events.admins_events_service import AdminsEventsService
from src.admins.keyboards.inline.admins_inline_keyboards import AdminsInlineKeyboards
from src.admins.keyboards.reply.admins_reply_keyboards import AdminsReplyKeyboards
from utils.lexicon.load_lexicon import load_lexicon
from utils.pagen.pagen_builder import PagenBuilder


class AdminsEventsController:
    def __init__(self):
        self.admins_service: AdminsEventsService = AdminsEventsService()
        self.admins_reply_keyboards: AdminsReplyKeyboards = AdminsReplyKeyboards()
        self.admins_inline_keyboards: AdminsInlineKeyboards = AdminsInlineKeyboards()

        self.pagen_builder: PagenBuilder = PagenBuilder()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

    async def admins_get_events(self, msg: Message, offset=0, edit=False) -> None:
        try:
            events = await self.admins_service.get_all_events(offset=offset)
            events_count = await self.admins_service.get_events_count()

            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard())

            pages = events_count[0][0]

            pagen_callback_data = f"_events-{offset}"

            if pages > 0:
                inline_callback_data = f"_events-{events[0][0]}"

                pagen = await self.pagen_builder.build_admin_pagen(
                    pages=pages,
                    offset=offset,
                    callback_data=pagen_callback_data
                )

                buttons = await self.admins_inline_keyboards.admins_dynamic_entity_keyboard(
                    callback_data=inline_callback_data
                )

                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        pagen,
                        buttons,
                        back_to_main_menu_btn
                    ])

                photo = events[0][1]

                msg_text = f"{offset + 1} из {pages}\n\n" \
                           f"Название: {events[0][2]}\n\n" \
                           f"Описание: {events[0][3]}\n\n" \
                           f"Дата проведения: {events[0][4]}\n\n" \
                           f"Ссылка: {events[0][5]}\n\n" \
                           f"Активность: {"Активно" if events[0][6]
                                                    else "Не активно"}"

                if edit:
                    media = InputMediaPhoto(media=photo, caption=msg_text)
                    await msg.edit_media(media=media, reply_markup=keyboard)
                else:
                    await msg.answer_photo(photo=photo,
                                           caption=msg_text,
                                           reply_markup=keyboard)
            else:
                inline_callback_data = f"_events"

                create_button = await self.admins_inline_keyboards.admins_dynamic_create_entity_keyboard(
                    callback_data=inline_callback_data
                )

                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    create_button,
                    back_to_main_menu_btn
                ])

                await msg.answer(self.replicas['admin']['other']['empty'],
                                 reply_markup=keyboard)
        except Exception as e:
            print(f"Error while getting events by admin: {e}")

            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)
