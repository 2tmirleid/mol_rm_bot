from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.admins.main_admins_controller import MainAdminsController
from src.admins.states.admins.create_admin_state import CreateAdminState
from src.admins.states.admins.edit_admin_state import EditAdminState
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


@router.message(Command("getchatid"))
async def process_admins_get_chat_id(msg: Message) -> None:
    await main_admins_controller.admins_get_chat_id(msg=msg)


@router.message(F.text == buttons['admin']['other']['to_main_panel'])
@router.callback_query(F.data == callback_data['admin']['other']['to_main_panel'])
async def process_get_admins_main_menu_panel(event: Message | CallbackQuery, state: FSMContext) -> None:
    await state.clear()

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


@router.callback_query(F.data == callback_data['admin']['general']['add'] + "_admins")
async def process_admins_add_admin_photo(clb_query: CallbackQuery, state: FSMContext) -> None:
    await main_admins_controller.admins_add_admin_photo(msg=clb_query.message, state=state)


@router.message(StateFilter(CreateAdminState.photo), F.photo)
async def process_admins_add_admin_chat_id(msg: Message, state: FSMContext) -> None:
    await main_admins_controller.admins_add_admin_chat_id(msg=msg, state=state)


@router.message(StateFilter(CreateAdminState.chat_id), F.text)
async def process_admins_add_admin_username(msg: Message, state: FSMContext) -> None:
    await main_admins_controller.admins_add_admin_username(msg=msg, state=state)


@router.message(StateFilter(CreateAdminState.username), F.text)
async def process_admins_add_admin_name(msg: Message, state: FSMContext) -> None:
    await main_admins_controller.admins_add_admin_name(msg=msg, state=state)


@router.message(StateFilter(CreateAdminState.name), F.text)
async def process_admins_add_admin_description(msg: Message, state: FSMContext) -> None:
    await main_admins_controller.admins_add_admin_description(msg=msg, state=state)


@router.message(StateFilter(CreateAdminState.description), F.text)
async def process_admins_add_admin_phone(msg: Message, state: FSMContext) -> None:
    await main_admins_controller.admins_add_admin_phone(msg=msg, state=state)


@router.message(StateFilter(CreateAdminState.phone), F.text)
async def process_admins_add_admin_finish(msg: Message, state: FSMContext) -> None:
    await main_admins_controller.admins_add_admin_finish(msg=msg, state=state)


@router.callback_query(lambda query: any(
    edit_action in query.data for edit_action in [
        callback_data['admin']['general']['delete'] + "_admins",
    ]
))
async def process_admins_delete_admin(clb_query: CallbackQuery) -> None:
    admin_id = str(clb_query.data.split("-")[1])

    await main_admins_controller.admins_delete_admin(msg=clb_query.message, admin_id=admin_id)


@router.callback_query(lambda query: query.data.startswith(
    callback_data['admin']['general']['edit']['main'] + "_admins"
))
async def process_admins_edit_admin(clb_query: CallbackQuery, state: FSMContext) -> None:
    admin_id = str(clb_query.data.split("-")[1])

    await main_admins_controller.admins_edit_admin(msg=clb_query.message,
                                                   state=state,
                                                   admin_id=admin_id)


@router.callback_query(lambda query: any(
    edit_action in query.data for edit_action in [
        callback_data['admin']['general']['edit']['photo'] + "_admins",
        callback_data['admin']['general']['edit']['name'] + "_admins",
        callback_data['admin']['general']['edit']['description'] + "_admins",
        callback_data['admin']['general']['edit']['phone'] + "_admins"
    ]
))
async def process_admins_edit_admin_property(clb_query: CallbackQuery, state: FSMContext) -> None:
    property = str(clb_query.data.split("_")[2])

    await main_admins_controller.admins_edit_admin_property(msg=clb_query.message, state=state, property=property)


@router.message(StateFilter(
    EditAdminState.value
), F.photo | F.text)
async def process_admins_edit_admin_value(msg: Message, state: FSMContext) -> None:
    await main_admins_controller.admins_edit_admin_value(msg=msg, state=state)
