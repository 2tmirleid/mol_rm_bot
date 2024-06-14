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
