from aiogram.types import Message, InlineKeyboardMarkup, InputMediaPhoto

from src.users.keyboards.inline.users_inline_keyboards import UsersInlineKeyboards
from src.users.keyboards.reply.users_reply_keyboards import UsersReplyKeyboards
from src.users.vacancies.users_vacancies_service import UsersVacanciesService
from utils.lexicon.load_lexicon import load_lexicon
from utils.pagen.pagen_builder import PagenBuilder


class UsersVacanciesController:
    def __init__(self):
        self.pagen_builder: PagenBuilder = PagenBuilder()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

        self.users_inline_keyboards: UsersInlineKeyboards = UsersInlineKeyboards()
        self.users_reply_keyboards: UsersReplyKeyboards = UsersReplyKeyboards()

        self.users_service: UsersVacanciesService = UsersVacanciesService()

    async def users_get_active_vacancies(self, msg: Message, offset=0, edit=False) -> None:
        try:
            vacancies = await self.users_service.get_active_vacancies(offset=offset)
            vacancies_count = await self.users_service.get_active_vacancies_count()

            pages = vacancies_count[0][0]

            pagen_callback_data = f"_vacancies-{offset}"

            if pages > 0:
                pagen = await self.pagen_builder.build_users_pagen(
                    pages=pages,
                    offset=offset,
                    callback_data=pagen_callback_data
                )

                button = await self.users_inline_keyboards.users_vacancies_entity_keyboard(url=vacancies[0][3])

                inline_keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        pagen,
                        button
                    ]
                )

                photo = vacancies[0][0]

                msg_text = f"{offset + 1} из {pages}\n\n" \
                           f"Название: {vacancies[0][1]}\n\n" \
                           f"Описание: {vacancies[0][2]}\n\n"

                if edit:
                    media = InputMediaPhoto(media=photo, caption=msg_text)
                    await msg.edit_media(media=media, reply_markup=inline_keyboard)
                else:
                    keyboard = await self.users_reply_keyboards.users_vacancies_panel_keyboard()

                    await msg.answer_photo(photo=photo,
                                           caption=msg_text,
                                           reply_markup=inline_keyboard)

                    await msg.answer(self.replicas['users']['other']['option'],
                                     reply_markup=keyboard)
            else:
                back_to_main_menu_btn = await (self.users_inline_keyboards.
                                               users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

                await msg.answer(self.replicas['users']['other']['empty'],
                                 reply_markup=back_to_main_menu_btn)

        except Exception as e:
            print(f"Error while getting vacancies by user: {e}")

            back_to_main_menu_btn = await (self.users_inline_keyboards.
                                           users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)

    async def users_take_part_vacancies(self, msg: Message) -> None:
        keyboard = await self.users_inline_keyboards.users_redirect_take_part_vacancies()
        main_menu_keyboard = await self.users_reply_keyboards.main_users_to_menu_panel_keyboard()

        await msg.answer(self.replicas['users']['other']['redirect'],
                         reply_markup=keyboard)

        await msg.answer(self.replicas['users']['other']['option'],
                         reply_markup=main_menu_keyboard)

    async def users_get_partners_vacancies(self, msg: Message) -> None:
        keyboard = await self.users_inline_keyboards.users_redirect_partners_vacancies()
        main_menu_keyboard = await self.users_reply_keyboards.main_users_to_menu_panel_keyboard()

        await msg.answer(self.replicas['users']['other']['redirect'],
                         reply_markup=keyboard)

        await msg.answer(self.replicas['users']['other']['option'],
                         reply_markup=main_menu_keyboard)
