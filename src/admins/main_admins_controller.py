import os
import re

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InputMediaPhoto
from dotenv import load_dotenv, find_dotenv

from src.admins.keyboards.inline.admins_inline_keyboards import AdminsInlineKeyboards
from src.admins.keyboards.reply.admins_reply_keyboards import AdminsReplyKeyboards
from src.admins.main_admins_service import MainAdminsService
from src.admins.states.admins.create_admin_state import CreateAdminState
from src.admins.states.admins.edit_admin_state import EditAdminState
from utils.lexicon.load_lexicon import load_lexicon
from utils.pagen.pagen_builder import PagenBuilder
from utils.validator import Validator


class MainAdminsController:
    def __init__(self):
        load_dotenv(find_dotenv())

        self.admins_reply_keyboards: AdminsReplyKeyboards = AdminsReplyKeyboards()
        self.admins_inline_keyboards: AdminsInlineKeyboards = AdminsInlineKeyboards()
        self.admins_service: MainAdminsService = MainAdminsService()

        self.pagen_builder: PagenBuilder = PagenBuilder()

        self.lexicon = load_lexicon()
        self.greeting = self.lexicon.get("greetings")
        self.replicas = self.lexicon.get("replicas")

        self.validator: Validator = Validator()

    async def admins_get_started(self, msg: Message) -> None:
        await msg.answer(f"{self.greeting['admin']}",
                         reply_markup=self.admins_reply_keyboards.main_admins_to_menu_panel_keyboard())

    async def get_main_admins_main_menu_panel(self, msg: Message) -> None:
        await msg.answer(f"{self.replicas['admin']['other']['option']}",
                         reply_markup=self.admins_reply_keyboards.main_admins_menu_panel_keyboard())

    async def admins_get_admins(self, msg: Message, offset=0, edit=False) -> None:
        try:
            admins = await self.admins_service.get_all_admins(offset=offset)
            admins_count = await self.admins_service.get_admins_count()

            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard())

            pages = admins_count[0][0]

            pagen_callback_data = f"_admins-{offset}"

            if pages > 0:
                inline_callback_data = f"_admins-{admins[0][0]}"

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

                photo = admins[0][1]

                msg_text = f"{offset + 1} из {pages}\n\n" \
                           f"Имя: {admins[0][2]}\n\n" \
                           f"Описание: {admins[0][3]}\n\n" \
                           f"Телефон: {admins[0][4]}\n\n" \

                if edit:
                    media = InputMediaPhoto(media=photo, caption=msg_text)
                    await msg.edit_media(media=media, reply_markup=keyboard)
                else:
                    await msg.answer_photo(photo=photo,
                                           caption=msg_text,
                                           reply_markup=keyboard)
            else:
                inline_callback_data = f"_admins"

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
            print(f"Error while getting admins by admin: {e}")

            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)

    async def admins_add_admin_photo(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        await msg.answer(self.replicas['admin']['entities']['create']['photo'],
                         reply_markup=back_to_main_menu_btn)

        await state.set_state(CreateAdminState.photo)

    async def admins_add_admin_chat_id(self, msg: Message, state: FSMContext) -> None:
        await state.update_data(photo=msg.photo[-1].file_id)

        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        await msg.answer(self.replicas['admin']['entities']['create']['chat_id'],
                         reply_markup=back_to_main_menu_btn)

        await state.set_state(CreateAdminState.chat_id)

    async def admins_add_admin_username(self, msg: Message, state: FSMContext) -> None:
        await state.update_data(chat_id=msg.text)

        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        await msg.answer(self.replicas['admin']['entities']['create']['username'],
                         reply_markup=back_to_main_menu_btn)

        await state.set_state(CreateAdminState.username)

    async def admins_add_admin_name(self, msg: Message, state: FSMContext) -> None:
        await state.update_data(username=msg.text)

        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        await msg.answer(self.replicas['admin']['entities']['create']['name'],
                         reply_markup=back_to_main_menu_btn)

        await state.set_state(CreateAdminState.name)

    async def admins_add_admin_description(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        is_valid, result = await self.validator.validate_title(title=msg.text)

        if not is_valid:
            await msg.answer(result)
            await msg.answer(self.replicas['admin']['entities']['create']['name'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateAdminState.name)
        else:
            await state.update_data(name=msg.text)

            await msg.answer(self.replicas['admin']['entities']['create']['description'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateAdminState.description)

    async def admins_add_admin_phone(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        is_valid, result = await self.validator.validate_description(description=msg.text)

        if not is_valid:
            await msg.answer(result)
            await msg.answer(self.replicas['admin']['entities']['create']['description'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateAdminState.description)
        else:
            await state.update_data(description=msg.text)

            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['admin']['entities']['create']['phone'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateAdminState.phone)

    async def admins_add_admin_finish(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        is_valid, result = await self.validator.validate_phone(phone=msg.text)

        if not is_valid:
            await msg.answer(result)
            await msg.answer(self.replicas['admin']['entities']['create']['phone'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateAdminState.phone)
        else:
            await state.update_data(phone=msg.text)

            data = await state.get_data()

            photo = data.get("photo")
            chat_id = data.get("chat_id")
            username = data.get("username")
            name = data.get("name")
            description = data.get("description")
            phone = data.get("phone")

            await state.clear()

            admin = [
                chat_id,
                username,
                photo,
                name,
                description,
                phone
            ]

            insert_admin = await self.admins_service.add_admin(admin=admin)

            if insert_admin:
                await msg.answer(self.replicas['admin']['entities']['create']['finish'])

                await self.admins_get_admins(msg=msg)
            else:
                await msg.answer(self.replicas['general']['error'],
                                 reply_markup=back_to_main_menu_btn)

    async def admins_delete_admin(self, msg: Message, admin_id: str) -> None:
        delete_admin = await self.admins_service.delete_admin(admin_id=admin_id)

        if delete_admin:
            await msg.answer(self.replicas['admin']['entities']['delete']['finish'])

            await self.admins_get_admins(msg=msg)
        else:
            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)

    async def admins_edit_admin(self, msg: Message, state: FSMContext, admin_id: str) -> None:
        await state.set_state(EditAdminState.admin_id)

        await state.update_data(admin_id=admin_id)

        callback_data = "_admins"

        edit_buttons = await (self.admins_inline_keyboards.
                              admins_dynamic_edit_entity_keyboard(callback_data=callback_data, admins=True))

        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard())

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            *edit_buttons,
            back_to_main_menu_btn
        ])

        await msg.answer(self.replicas['admin']['entities']['edit']['property'],
                         reply_markup=keyboard)

        await state.set_state(EditAdminState.property)

    async def admins_edit_admin_property(self, msg: Message, state: FSMContext, property: str) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        await state.update_data(property=property)

        await msg.answer(self.replicas['admin']['entities']['edit']['value'],
                         reply_markup=back_to_main_menu_btn)

        await state.set_state(EditAdminState.value)

    async def admins_edit_admin_value(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        data = await state.get_data()

        admin_id = data.get("admin_id")
        property = data.get("property")
        value = ""

        if property == "photo":
            if msg.photo[-1].file_id:
                value = msg.photo[-1].file_id
        elif property == "name":
            is_valid, result = await self.validator.validate_title(title=msg.text)

            if not is_valid:
                await msg.answer(result)
                await msg.answer(self.replicas['admin']['entities']['edit']['value'],
                                 reply_markup=back_to_main_menu_btn)

                await state.set_state(EditAdminState.value)

                return
            else:
                value = msg.text

        elif property == "description":
            is_valid, result = await self.validator.validate_description(description=msg.text)

            if not is_valid:
                await msg.answer(result)
                await msg.answer(self.replicas['admin']['entities']['edit']['value'],
                                 reply_markup=back_to_main_menu_btn)

                await state.set_state(EditAdminState.value)

                return
            else:
                value = msg.text

        elif property == "phone":
            is_valid, result = await self.validator.validate_phone(phone=msg.text)

            if not is_valid:
                await msg.answer(result)
                await msg.answer(self.replicas['admin']['entities']['edit']['value'],
                                 reply_markup=back_to_main_menu_btn)

                await state.set_state(EditAdminState.value)

                return
            else:
                value = msg.text

        update_admin = await self.admins_service.edit_admin(
            admin_id=admin_id, property=property, value=value
        )

        await state.clear()

        if update_admin:
            await msg.answer(self.replicas['admin']['entities']['edit']['finish'],
                             await self.admins_get_admins(msg=msg))
        else:
            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)
