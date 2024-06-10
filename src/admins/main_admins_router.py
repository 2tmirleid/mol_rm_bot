from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from src.admins.main_admins_controller import MainAdminsController
from src.middlewares.admins_middleware import AdminsMiddleware
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()
router.message.middleware(AdminsMiddleware())

lexicon = load_lexicon()
buttons = lexicon.get("buttons")

main_admins_controller: MainAdminsController = MainAdminsController()


@router.message(Command("admin"))
async def process_admins_get_started(msg: Message) -> None:
    await main_admins_controller.admins_get_started(msg)


@router.message(F.text == buttons["admin"]["other"]["to_main_panel"])
async def process_get_admins_main_menu_panel(msg: Message) -> None:
    await main_admins_controller.get_main_admins_main_menu_panel(msg)
