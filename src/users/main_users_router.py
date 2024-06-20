from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.users.main_users_controller import MainUsersController
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

lexicon = load_lexicon()
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")

main_users_controller: MainUsersController = MainUsersController()


@router.message(Command("start"))
async def process_users_get_started(msg: Message) -> None:
    await main_users_controller.users_get_started(msg=msg)


@router.message(Command("getchatid"))
async def process_admins_get_chat_id(msg: Message) -> None:
    await main_users_controller.users_get_chat_id(msg=msg)


@router.message(F.text == buttons['users']['other']['to_main_panel'])
@router.callback_query(F.data == callback_data['users']['other']['to_main_panel'])
async def process_get_users_main_menu_panel(event: Message | CallbackQuery) -> None:
    if isinstance(event, Message):
        msg = event

        await main_users_controller.get_main_users_main_menu_panel(msg)
    elif isinstance(event, CallbackQuery):
        msg = event.message

        await main_users_controller.get_main_users_main_menu_panel(msg)


