import os

from aiogram.types import Message, InlineKeyboardMarkup, InputMediaPhoto, FSInputFile, InlineKeyboardButton
from aiogram.utils.media_group import MediaGroupBuilder

from src.users.keyboards.inline.users_inline_keyboards import UsersInlineKeyboards
from src.users.keyboards.reply.users_reply_keyboards import UsersReplyKeyboards
from src.users.programs.users_programs_service import UsersProgramsService
from utils.lexicon.load_lexicon import load_lexicon
from utils.pagen.pagen_builder import PagenBuilder


class UsersProgramsController:
    def __init__(self):
        self.pagen_builder: PagenBuilder = PagenBuilder()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

        self.users_inline_keyboards: UsersInlineKeyboards = UsersInlineKeyboards()
        self.users_reply_keyboards: UsersReplyKeyboards = UsersReplyKeyboards()

        self.users_service: UsersProgramsService = UsersProgramsService()

    async def users_get_active_programs(self, msg: Message) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))

        file1 = os.path.join(current_dir, '..', '..', 'static', 'programs', '1.jpg')
        file2 = os.path.join(current_dir, '..', '..', 'static', 'programs', '2.jpg')
        file3 = os.path.join(current_dir, '..', '..', 'static', 'programs', '3.jpg')
        file4 = os.path.join(current_dir, '..', '..', 'static', 'programs', '4.jpg')

        # caption = await self.users_service.get_program_description()
        caption = ("И это одна из самых интересных молодёжных программ на этот год. "
                   "Мы предлагаем вам стать Амбассадорами нашей команды – проводниками молодых в "
                   "нашу событийную историю. "
                   "Но чтобы войти в состав команды проводников, нужно представиться…")

        # print(caption)

        media = MediaGroupBuilder(caption=caption)

        media.add_photo(FSInputFile(file1))
        media.add_photo(FSInputFile(file2))
        media.add_photo(FSInputFile(file3))
        media.add_photo(FSInputFile(file4))

        await msg.answer_media_group(media=media.build())
        # reply_parameters=keyboard

        keyboard = [
            [InlineKeyboardButton(text='Рассказать о себе', callback_data='users_program_tell_about')],
            # [InlineKeyboardButton(text='Положение о Конкурсной программе', callback_data='users_program_get_file')],
            await self.users_inline_keyboards.users_dynamic_entity_to_main_menu_panel_keyboard()
        ]

        await msg.answer(self.replicas['users']['other']['option'],
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=keyboard
                         ))

    async def users_tell_about(self, msg: Message):
        await msg.answer(
            'Представься, расскажи, как тебя зовут, сколько тебе лет и где же ты учишься или работаешь. Добавь, чем ты занимаешься и какими навыками обладаешь. И главный вопрос - почему именно Ты должен стать проводником молодых. Всё остальное на ваше усмотрение – грузи визитку на облачное хранилище и отправляй нам',
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='Загрузить видео-визитку',
                                          url='https://forms.yandex.ru/u/6790edb902848f5f77e55699/')],
                    await self.users_inline_keyboards.users_dynamic_entity_to_main_menu_panel_keyboard()
                ])
            )

    # async def users_get_active_programs(self, msg: Message, offset=0, edit=False) -> None:
    #     try:
    #         back_to_main_menu_btn = await (self.users_inline_keyboards.
    #                                        users_dynamic_entity_to_main_menu_panel_keyboard())
    #
    #         programs = await self.users_service.get_active_programs(offset=offset)
    #         programs_count = await self.users_service.get_active_programs_count()
    #
    #         pages = programs_count[0][0]
    #
    #         pagen_callback_data = f"_programs-{offset}"
    #
    #         if pages > 0:
    #             pagen = await self.pagen_builder.build_users_pagen(
    #                 pages=pages,
    #                 offset=offset,
    #                 callback_data=pagen_callback_data
    #             )
    #
    #             button = await self.users_inline_keyboards.users_programs_entity_keyboard(url=programs[0][3])
    #
    #             inline_keyboard = InlineKeyboardMarkup(
    #                 inline_keyboard=[
    #                     pagen,
    #                     button
    #                 ]
    #             )
    #
    #             photo = programs[0][0]
    #
    #             msg_text = f"{offset + 1} из {pages}\n\n" \
    #                        f"<b>{programs[0][1]}</b>\n\n" \
    #                        f"{programs[0][2]}\n\n"
    #
    #             if edit:
    #                 media = InputMediaPhoto(media=photo, caption=msg_text, parse_mode="HTML")
    #                 await msg.edit_media(media=media, reply_markup=inline_keyboard)
    #             else:
    #                 keyboard = await self.users_reply_keyboards.users_programs_panel_keyboard()
    #
    #                 await msg.answer_photo(photo=photo,
    #                                        caption=msg_text,
    #                                        reply_markup=inline_keyboard,
    #                                        parse_mode="HTML")
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
    #         print(f"Error while getting programs by user: {e}")
    #
    #         back_to_main_menu_btn = await (self.users_inline_keyboards.
    #                                        users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))
    #
    #         await msg.answer(self.replicas['general']['error'],
    #                          reply_markup=back_to_main_menu_btn)

    async def users_get_useful_docs(self, msg: Message) -> None:
        keyboard = await self.users_inline_keyboards.users_redirect_to_useful_docs()
        main_menu_keyboard = await self.users_reply_keyboards.main_users_to_menu_panel_keyboard()

        await msg.answer(self.replicas['users']['other']['redirect'],
                         reply_markup=keyboard)

        await msg.answer(self.replicas['users']['other']['option'],
                         reply_markup=main_menu_keyboard)
