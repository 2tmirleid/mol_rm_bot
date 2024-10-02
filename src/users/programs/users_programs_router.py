from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from src.users.programs.users_programs_controller import UsersProgramsController
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

lexicon = load_lexicon()
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")

users_programs_controller: UsersProgramsController = UsersProgramsController()


@router.message(F.text == buttons['users']['main_panel']['programs'])
async def process_users_get_programs(msg: Message) -> None:
    await users_programs_controller.users_get_active_programs(msg=msg)


@router.message(F.text == buttons['users']['programs']['useful'])
async def process_users_get_useful_docs(msg: Message) -> None:
    await users_programs_controller.users_get_useful_docs(msg=msg)


@router.callback_query(F.data == 'users_program_tell_about')
async def process_users_tell_about(clb_query: CallbackQuery):
    await users_programs_controller.users_tell_about(clb_query.message)

# @router.callback_query(lambda query: query.data.startswith("users_pagen_next_programs"))
# async def process_users_pagen_next_programs(clb_query: CallbackQuery) -> None:
#     offset_split = str(clb_query.data.split("-")[1])
#
#     offset = int(offset_split) + 1
#
#     await users_programs_controller.users_get_active_programs(msg=clb_query.message,
#                                                               offset=offset,
#                                                               edit=True)
#
#
# @router.callback_query(lambda query: query.data.startswith("users_pagen_backward_programs"))
# async def process_users_pagen_backward_programs(clb_query: CallbackQuery) -> None:
#     offset_split = str(clb_query.data.split("-")[1])
#     offset = int(offset_split) - 1
#
#     await users_programs_controller.users_get_active_programs(msg=clb_query.message,
#                                                               offset=offset,
#                                                               edit=True)

