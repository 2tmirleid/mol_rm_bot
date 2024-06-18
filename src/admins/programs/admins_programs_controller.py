import os
import re

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from dotenv import load_dotenv, find_dotenv

from src.admins.keyboards.inline.admins_inline_keyboards import AdminsInlineKeyboards
from src.admins.keyboards.reply.admins_reply_keyboards import AdminsReplyKeyboards
from src.admins.programs.admins_programs_service import AdminsProgramsService
from src.admins.states.programs.create_program_state import CreateProgramState
from src.admins.states.programs.edit_program_state import EditProgramState
from utils.lexicon.load_lexicon import load_lexicon
from utils.pagen.pagen_builder import PagenBuilder
from utils.validator import Validator


class AdminsProgramsController:
    def __init__(self):
        load_dotenv(find_dotenv())

        self.admins_service: AdminsProgramsService = AdminsProgramsService()
        self.admins_reply_keyboards: AdminsReplyKeyboards = AdminsReplyKeyboards()
        self.admins_inline_keyboards: AdminsInlineKeyboards = AdminsInlineKeyboards()

        self.pagen_builder: PagenBuilder = PagenBuilder()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

        self.validator: Validator = Validator()

    async def admins_get_programs(self, msg: Message, offset=0, edit=False) -> None:
        try:
            programs = await self.admins_service.get_all_programs(offset=offset)
            programs_count = await self.admins_service.get_programs_count()

            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard())

            pages = programs_count[0][0]

            pagen_callback_data = f"_programs-{offset}"

            if pages > 0:
                inline_callback_data = f"_programs-{programs[0][0]}"

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

                photo = programs[0][1]

                msg_text = f"{offset + 1} из {pages}\n\n" \
                           f"Название: {programs[0][2]}\n\n" \
                           f"Описание: {programs[0][3]}\n\n" \
                           f"Ссылка: {programs[0][4]}\n\n" \
                           f"Активность: {"Активно" if programs[0][5]
                                                    else "Не активно"}"

                if edit:
                    media = InputMediaPhoto(media=photo, caption=msg_text)
                    await msg.edit_media(media=media, reply_markup=keyboard)
                else:
                    await msg.answer_photo(photo=photo,
                                           caption=msg_text,
                                           reply_markup=keyboard)
            else:
                inline_callback_data = f"_programs"

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
            print(f"Error while getting programs by admin: {e}")

            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)

    async def admins_add_program_photo(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        await msg.answer(self.replicas['admin']['entities']['create']['photo'],
                         reply_markup=back_to_main_menu_btn)

        await state.set_state(CreateProgramState.photo)

    async def admins_add_program_title(self, msg: Message, state: FSMContext) -> None:
        await state.update_data(photo=msg.photo[-1].file_id)

        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        await msg.answer(self.replicas['admin']['entities']['create']['title'],
                         reply_markup=back_to_main_menu_btn)

        await state.set_state(CreateProgramState.title)

    async def admins_add_program_description(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        is_valid, result = await self.validator.validate_title(title=msg.text)

        if not is_valid:
            await msg.answer(result)
            await msg.answer(self.replicas['admin']['entities']['create']['title'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateProgramState.title)
        else:
            await state.update_data(title=msg.text)

            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['admin']['entities']['create']['description'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateProgramState.description)

    async def admins_add_program_link(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        is_valid, result = await self.validator.validate_description(description=msg.text)

        if not is_valid:
            await msg.answer(result)
            await msg.answer(self.replicas['admin']['entities']['create']['description'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateProgramState.description)
        else:
            await state.update_data(description=msg.text)

            await msg.answer(self.replicas['admin']['entities']['create']['link'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateProgramState.link)

    async def admins_add_program_finish(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        is_valid, result = await self.validator.validate_link(link=msg.text)

        if not is_valid:
            await msg.answer(result)
            await msg.answer(self.replicas['admin']['entities']['create']['link'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateProgramState.link)
        else:
            await state.update_data(link=msg.text)

            data = await state.get_data()

            photo = data.get("photo")
            title = data.get("title")
            description = data.get("description")
            link = data.get("link")

            await state.clear()

            program = [
                photo,
                title,
                description,
                link
            ]

            insert_program = await self.admins_service.add_program(program=program)

            if insert_program:
                await msg.answer(self.replicas['admin']['entities']['create']['finish'])

                await self.admins_get_programs(msg=msg)
            else:
                back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                               admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

                await msg.answer(self.replicas['general']['error'],
                                 reply_markup=back_to_main_menu_btn)

    async def admins_delete_program(self, msg: Message, program_id: str) -> None:
        delete_program = await self.admins_service.delete_program(program_id=program_id)

        if delete_program:
            await msg.answer(self.replicas['admin']['entities']['delete']['finish'])

            await self.admins_get_programs(msg=msg)
        else:
            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)

    async def admins_edit_program(self, msg: Message, state: FSMContext, program_id: str) -> None:
        await state.set_state(EditProgramState.program_id)

        await state.update_data(program_id=program_id)

        callback_data = "_programs"

        edit_buttons = await (self.admins_inline_keyboards.
                              admins_dynamic_edit_entity_keyboard(callback_data=callback_data))

        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard())

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            *edit_buttons,
            back_to_main_menu_btn
        ])

        await msg.answer(self.replicas['admin']['entities']['edit']['property'],
                         reply_markup=keyboard)

        await state.set_state(EditProgramState.property)

    async def admins_edit_program_property(self, msg: Message, state: FSMContext, property: str) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        if property == "activity":
            data = await state.get_data()

            program_id = data.get("program_id")

            await state.clear()

            program_activity = await self.admins_service.change_program_activity(program_id=program_id)

            if program_activity:
                await msg.answer(self.replicas['admin']['entities']['edit']['finish'])

                await self.admins_get_programs(msg=msg)
            else:
                await msg.answer(self.replicas['general']['error'],
                                 reply_markup=back_to_main_menu_btn)
        else:
            await state.update_data(property=property)

            await msg.answer(self.replicas['admin']['entities']['edit']['value'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(EditProgramState.value)

    async def admins_edit_program_value(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        data = await state.get_data()

        program_id = data.get("program_id")
        property = data.get("property")
        value = ""

        if property == "photo":
            if msg.photo[-1].file_id:
                value = msg.photo[-1].file_id
        elif property == "title":
            is_valid, result = await self.validator.validate_title(title=msg.text)

            if not is_valid:
                await msg.answer(result)
                await msg.answer(self.replicas['admin']['entities']['edit']['value'],
                                 reply_markup=back_to_main_menu_btn)

                await state.set_state(EditProgramState.value)

                return
            else:
                value = msg.text

        elif property == "description":
            is_valid, result = await self.validator.validate_description(description=msg.text)

            if not is_valid:
                await msg.answer(result)
                await msg.answer(self.replicas['admin']['entities']['edit']['value'],
                                 reply_markup=back_to_main_menu_btn)

                await state.set_state(EditProgramState.value)

                return
            else:
                value = msg.text

        elif property == "link":
            is_valid, result = await self.validator.validate_link(link=msg.text)

            if not is_valid:
                await msg.answer(result)
                await msg.answer(self.replicas['admin']['entities']['edit']['value'],
                                 reply_markup=back_to_main_menu_btn)

                await state.set_state(EditProgramState.value)

                return
            else:
                value = msg.text

        update_program = await self.admins_service.edit_program(
            program_id=program_id, property=property, value=value
        )

        await state.clear()

        if update_program:
            await msg.answer(self.replicas['admin']['entities']['edit']['finish'],
                             await self.admins_get_programs(msg=msg))
        else:
            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)
