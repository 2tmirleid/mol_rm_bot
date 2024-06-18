import os
import re

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InputMediaPhoto
from dotenv import load_dotenv, find_dotenv

from src.admins.keyboards.inline.admins_inline_keyboards import AdminsInlineKeyboards
from src.admins.keyboards.reply.admins_reply_keyboards import AdminsReplyKeyboards
from src.admins.states.vacancies.create_vacancy_state import CreateVacancyState
from src.admins.states.vacancies.edit_vacancy_state import EditVacancyState
from src.admins.vacancies.admins_vacancies_service import AdminsVacanciesService
from utils.lexicon.load_lexicon import load_lexicon
from utils.pagen.pagen_builder import PagenBuilder
from utils.validator import Validator


class AdminsVacanciesController:
    def __init__(self):
        load_dotenv(find_dotenv())

        self.admins_service: AdminsVacanciesService = AdminsVacanciesService()
        self.admins_reply_keyboards: AdminsReplyKeyboards = AdminsReplyKeyboards()
        self.admins_inline_keyboards: AdminsInlineKeyboards = AdminsInlineKeyboards()

        self.pagen_builder: PagenBuilder = PagenBuilder()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

        self.validator: Validator = Validator()

    async def admins_get_vacancies(self, msg: Message, offset=0, edit=False) -> None:
        try:
            vacancies = await self.admins_service.get_all_vacancies(offset=offset)
            vacancies_count = await self.admins_service.get_vacancies_count()

            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard())

            pages = vacancies_count[0][0]

            pagen_callback_data = f"_vacancies-{offset}"

            if pages > 0:
                inline_callback_data = f"_vacancies-{vacancies[0][0]}"

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

                photo = vacancies[0][1]

                msg_text = f"{offset + 1} из {pages}\n\n" \
                           f"Название: {vacancies[0][2]}\n\n" \
                           f"Описание: {vacancies[0][3]}\n\n" \
                           f"Ссылка: {vacancies[0][4]}\n\n" \
                           f"Активность: {"Активно" if vacancies[0][5]
                                                    else "Не активно"}"

                if edit:
                    media = InputMediaPhoto(media=photo, caption=msg_text)
                    await msg.edit_media(media=media, reply_markup=keyboard)
                else:
                    await msg.answer_photo(photo=photo,
                                           caption=msg_text,
                                           reply_markup=keyboard)
            else:
                inline_callback_data = f"_vacancies"

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
            print(f"Error while getting vacancies by admin: {e}")

            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)

    async def admins_add_vacancy_photo(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        await msg.answer(self.replicas['admin']['entities']['create']['photo'],
                         reply_markup=back_to_main_menu_btn)

        await state.set_state(CreateVacancyState.photo)

    async def admins_add_vacancy_title(self, msg: Message, state: FSMContext) -> None:
        await state.update_data(photo=msg.photo[-1].file_id)

        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        await msg.answer(self.replicas['admin']['entities']['create']['title'],
                         reply_markup=back_to_main_menu_btn)

        await state.set_state(CreateVacancyState.title)

    async def admins_add_vacancy_description(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        is_valid, result = await self.validator.validate_title(title=msg.text)

        if not is_valid:
            await msg.answer(result)
            await msg.answer(self.replicas['admin']['entities']['create']['title'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateVacancyState.title)
        else:
            await state.update_data(title=msg.text)

            await msg.answer(self.replicas['admin']['entities']['create']['description'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateVacancyState.description)

    async def admins_add_vacancy_link(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        is_valid, result = await self.validator.validate_description(description=msg.text)

        if not is_valid:
            await msg.answer(result)
            await msg.answer(self.replicas['admin']['entities']['create']['description'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateVacancyState.description)
        else:
            await state.update_data(description=msg.text)

            await msg.answer(self.replicas['admin']['entities']['create']['link'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateVacancyState.link)

    async def admins_add_vacancy_finish(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        is_valid, result = await self.validator.validate_link(link=msg.text)

        if not is_valid:
            await msg.answer(result)
            await msg.answer(self.replicas['admin']['entities']['create']['link'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateVacancyState.link)
        else:
            await state.update_data(link=msg.text)

            data = await state.get_data()

            photo = data.get("photo")
            title = data.get("title")
            description = data.get("description")
            link = data.get("link")

            await state.clear()

            vacancy = [
                photo,
                title,
                description,
                link
            ]

            insert_vacancy = await self.admins_service.add_vacancy(vacancy=vacancy)

            if insert_vacancy:
                await msg.answer(self.replicas['admin']['entities']['create']['finish'])

                await self.admins_get_vacancies(msg=msg)
            else:
                back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                               admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

                await msg.answer(self.replicas['general']['error'],
                                 reply_markup=back_to_main_menu_btn)

    async def admins_delete_vacancy(self, msg: Message, vacancy_id: str) -> None:
        delete_vacancy = await self.admins_service.delete_vacancy(vacancy_id=vacancy_id)

        if delete_vacancy:
            await msg.answer(self.replicas['admin']['entities']['delete']['finish'])

            await self.admins_get_vacancies(msg=msg)
        else:
            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)

    async def admins_edit_vacancy(self, msg: Message, state: FSMContext, vacancy_id: str) -> None:
        await state.set_state(EditVacancyState.vacancy_id)

        await state.update_data(vacancy_id=vacancy_id)

        callback_data = "_vacancies"

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

        await state.set_state(EditVacancyState.property)

    async def admins_edit_vacancy_property(self, msg: Message, state: FSMContext, property: str) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        if property == "activity":
            data = await state.get_data()

            vacancy_id = data.get("vacancy_id")

            await state.clear()

            vacancy_activity = await self.admins_service.change_vacancy_activity(vacancy_id=vacancy_id)

            if vacancy_activity:
                await msg.answer(self.replicas['admin']['entities']['edit']['finish'])

                await self.admins_get_vacancies(msg=msg)
            else:
                await msg.answer(self.replicas['general']['error'],
                                 reply_markup=back_to_main_menu_btn)
        else:
            await state.update_data(property=property)

            await msg.answer(self.replicas['admin']['entities']['edit']['value'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(EditVacancyState.value)

    async def admins_edit_vacancy_value(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        data = await state.get_data()

        vacancy_id = data.get("vacancy_id")
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

                await state.set_state(EditVacancyState.value)

                return
            else:
                value = msg.text

        elif property == "description":
            is_valid, result = await self.validator.validate_description(description=msg.text)

            if not is_valid:
                await msg.answer(result)
                await msg.answer(self.replicas['admin']['entities']['edit']['value'],
                                 reply_markup=back_to_main_menu_btn)

                await state.set_state(EditVacancyState.value)

                return
            else:
                value = msg.text

        elif property == "link":
            is_valid, result = await self.validator.validate_link(link=msg.text)

            if not is_valid:
                await msg.answer(result)
                await msg.answer(self.replicas['admin']['entities']['edit']['value'],
                                 reply_markup=back_to_main_menu_btn)

                await state.set_state(EditVacancyState.value)

                return
            else:
                value = msg.text

        update_vacancy = await self.admins_service.edit_vacancy(
            vacancy_id=vacancy_id, property=property, value=value
        )

        await state.clear()

        if update_vacancy:
            await msg.answer(self.replicas['admin']['entities']['edit']['finish'],
                             await self.admins_get_vacancies(msg=msg))
        else:
            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)
