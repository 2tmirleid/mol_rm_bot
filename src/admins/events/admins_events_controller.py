import os
import re

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InputMediaPhoto
from dotenv import load_dotenv, find_dotenv

from src.admins.events.admins_events_service import AdminsEventsService
from src.admins.keyboards.inline.admins_inline_keyboards import AdminsInlineKeyboards
from src.admins.keyboards.reply.admins_reply_keyboards import AdminsReplyKeyboards
from src.admins.states.events.create_event_state import CreateEventState
from utils.lexicon.load_lexicon import load_lexicon
from utils.pagen.pagen_builder import PagenBuilder


class AdminsEventsController:
    def __init__(self):
        load_dotenv(find_dotenv())

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

    async def admins_add_event_photo(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        await msg.answer(self.replicas['admin']['entities']['create']['photo'],
                         reply_markup=back_to_main_menu_btn)

        await state.set_state(CreateEventState.photo)

    async def admins_add_event_title(self, msg: Message, state: FSMContext) -> None:
        await state.update_data(photo=msg.photo[-1].file_id)

        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        await msg.answer(self.replicas['admin']['entities']['create']['title'],
                         reply_markup=back_to_main_menu_btn)

        await state.set_state(CreateEventState.title)

    async def admins_add_event_description(self, msg: Message, state: FSMContext) -> None:
        await state.update_data(title=msg.text)

        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        await msg.answer(self.replicas['admin']['entities']['create']['description'],
                         reply_markup=back_to_main_menu_btn)

        await state.set_state(CreateEventState.description)

    async def admins_add_event_date(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        max_chars_length = os.environ["MAX_CHARS_LENGTH"]
        chars_length = re.findall(r".", msg.text)

        if len(chars_length) > int(max_chars_length):
            await msg.answer(self.replicas['general']['max_chars_length'] + f" {max_chars_length}")
            await msg.answer(self.replicas['admin']['entities']['create']['description'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateEventState.description)
        else:
            await state.update_data(description=msg.text)

            await msg.answer(self.replicas['admin']['entities']['create']['date'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateEventState.event_date)

    async def admins_add_event_link(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        date_pattern = r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(19|20)\d\d$"

        if bool(re.match(date_pattern, msg.text)):
            await state.update_data(event_date=msg.text)

            await msg.answer(self.replicas['admin']['entities']['create']['link'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateEventState.link)
        else:
            await msg.answer(self.replicas['general']['date_pattern'])
            await msg.answer(self.replicas['admin']['entities']['create']['date'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateEventState.event_date)

    async def admins_add_event_finish(self, msg: Message, state: FSMContext) -> None:
        await state.update_data(link=msg.text)

        data = await state.get_data()

        photo = data.get("photo")
        title = data.get("title")
        description = data.get("description")
        event_date = data.get("event_date")
        link = data.get("link")

        await state.clear()

        event = [
            photo,
            title,
            description,
            event_date,
            link
        ]

        insert_event = await self.admins_service.add_event(event=event)

        if insert_event:
            await msg.answer(self.replicas['admin']['entities']['create']['finish'])

            await self.admins_get_events(msg=msg)
        else:
            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)
