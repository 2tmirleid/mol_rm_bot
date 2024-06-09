from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.admins.commands.admins_commands_controller import AdminsCommandsController

router: Router = Router()

admins_commands_controller: AdminsCommandsController = AdminsCommandsController()


@router.message(Command("admin"))
async def process_get_main_admin_panel(msg: Message) -> None:
    await admins_commands_controller.get_main_admin_panel(msg)
