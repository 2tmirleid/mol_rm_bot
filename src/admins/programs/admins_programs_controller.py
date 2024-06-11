from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from src.admins.keyboards.inline.admins_inline_keyboards import AdminsInlineKeyboards
from src.admins.keyboards.reply.admins_reply_keyboards import AdminsReplyKeyboards
from src.admins.programs.admins_programs_service import AdminsProgramsService
from utils.lexicon.load_lexicon import load_lexicon
from utils.pagen.pagen_builder import PagenBuilder


class AdminsProgramsController:
    def __init__(self):
        self.admins_service: AdminsProgramsService = AdminsProgramsService()
        self.admins_reply_keyboards: AdminsReplyKeyboards = AdminsReplyKeyboards()
        self.admins_inline_keyboards: AdminsInlineKeyboards = AdminsInlineKeyboards()

        self.pagen_builder: PagenBuilder = PagenBuilder()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

    async def admins_get_programs(self, msg: Message, offset=0, edit=False) -> None:
        try:
            programs = await self.admins_service.get_all_programs(offset=offset)
            programs_count = await self.admins_service.get_programs_count()

            pages = programs_count[0][0]

            pagen_callback_data = f"_programs-{offset}"
            inline_callback_data = f"_programs-{programs[0][0]}"

            if pages > 0:
                pagen = await self.pagen_builder.build(
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
                        buttons
                    ])

                msg_text = f"{offset + 1} из {pages}\n\n" \
                           f"Описание: {programs[0][2]}\n" \
                           f"Ссылка: {programs[0][3]}"

                if edit:
                    await msg.edit_text(msg_text,
                                        reply_markup=keyboard)
                else:
                    await msg.answer(msg_text,
                                     reply_markup=keyboard)
            else:
                create_button = await self.admins_inline_keyboards.admins_dynamic_create_entity_keyboard(
                    callback_data=inline_callback_data
                )

                keyboard = InlineKeyboardMarkup(inline_keyboard=[create_button])

                await msg.answer(self.replicas['admin']['other']['unfounded'],
                                 reply_markup=keyboard)
        except Exception as e:
            print(f"Error while getting programs by admin: {e}")
