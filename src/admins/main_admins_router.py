from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from src.admins.main_admins_controller import MainAdminsController
from src.middlewares.admins_middleware import AdminsMiddleware
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()
router.message.middleware(AdminsMiddleware())

lexicon = load_lexicon()
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")

main_admins_controller: MainAdminsController = MainAdminsController()


@router.message(Command("admin"))
async def process_admins_get_started(msg: Message) -> None:
    await main_admins_controller.admins_get_started(msg)


@router.message(F.text == buttons['admin']['other']['to_main_panel'])
@router.callback_query(F.data == callback_data['admin']['other']['to_main_panel'])
async def process_get_admins_main_menu_panel(event: Message | CallbackQuery) -> None:
    if isinstance(event, Message):
        msg = event

        await main_admins_controller.get_main_admins_main_menu_panel(msg)
    elif isinstance(event, CallbackQuery):
        msg = event.message

        await main_admins_controller.get_main_admins_main_menu_panel(msg)


@router.message(F.text == buttons["admin"]["main_panel"]["admins"])
async def process_admins_get_programs(msg: Message) -> None:
    await main_admins_controller.admins_get_admins(msg)


@router.callback_query(lambda query: query.data.startswith("admins_pagen_next_admins"))
async def process_admins_pagen_next_admins(clb_query: CallbackQuery) -> None:
    offset_split = str(clb_query.data.split("-")[1])

    offset = int(offset_split) + 1

    await main_admins_controller.admins_get_admins(msg=clb_query.message,
                                                   offset=offset,
                                                   edit=True)


@router.callback_query(lambda query: query.data.startswith("admins_pagen_backward_admins"))
async def process_admins_pagen_backward_admins(clb_query: CallbackQuery) -> None:
    offset_split = str(clb_query.data.split("-")[1])
    offset = int(offset_split) - 1

    await main_admins_controller.admins_get_admins(msg=clb_query.message,
                                                   offset=offset,
                                                   edit=True)
