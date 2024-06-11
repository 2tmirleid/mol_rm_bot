from aiogram import Router, F, types
from aiogram.types import Message

from src.admins.programs.admins_programs_controller import AdminsProgramsController
from src.middlewares.admins_middleware import AdminsMiddleware
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()
router.message.middleware(AdminsMiddleware())

admins_programs_controller: AdminsProgramsController = AdminsProgramsController()

lexicon = load_lexicon()
buttons = lexicon.get("buttons")


@router.message(F.text == buttons["admin"]["main_panel"]["programs"])
async def process_admins_get_programs(msg: Message) -> None:
    await admins_programs_controller.admins_get_programs(msg)


@router.callback_query(lambda query: query.data.startswith("admins_pagen_next_programs"))
async def process_admins_pagen_next_programs(clb_query: types.CallbackQuery):
    offset_split = str(clb_query.data.split("-")[1])

    offset = int(offset_split) + 1

    await admins_programs_controller.admins_get_programs(msg=clb_query.message,
                                                         offset=offset,
                                                         edit=True)


@router.callback_query(lambda query: query.data.startswith("admins_pagen_backward_programs"))
async def process_admins_pagen_backward_programs(clb_query: types.CallbackQuery):
    offset_split = str(clb_query.data.split("-")[1])
    offset = int(offset_split) - 1

    await admins_programs_controller.admins_get_programs(msg=clb_query.message,
                                                         offset=offset,
                                                         edit=True)
