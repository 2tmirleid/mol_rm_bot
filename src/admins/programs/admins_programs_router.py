from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.admins.programs.admins_programs_controller import AdminsProgramsController
from src.admins.states.programs.create_program_state import CreateProgramState
from src.admins.states.programs.edit_program_state import EditProgramState
from src.middlewares.admins_middleware import AdminsMiddleware
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()
router.message.middleware(AdminsMiddleware())

admins_programs_controller: AdminsProgramsController = AdminsProgramsController()

lexicon = load_lexicon()
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")


@router.message(F.text == buttons["admin"]["main_panel"]["programs"])
async def process_admins_get_programs(msg: Message) -> None:
    await admins_programs_controller.admins_get_programs(msg)


@router.callback_query(lambda query: query.data.startswith("admins_pagen_next_programs"))
async def process_admins_pagen_next_programs(clb_query: CallbackQuery) -> None:
    offset_split = str(clb_query.data.split("-")[1])

    offset = int(offset_split) + 1

    await admins_programs_controller.admins_get_programs(msg=clb_query.message,
                                                         offset=offset,
                                                         edit=True)


@router.callback_query(lambda query: query.data.startswith("admins_pagen_backward_programs"))
async def process_admins_pagen_backward_programs(clb_query: CallbackQuery) -> None:
    offset_split = str(clb_query.data.split("-")[1])
    offset = int(offset_split) - 1

    await admins_programs_controller.admins_get_programs(msg=clb_query.message,
                                                         offset=offset,
                                                         edit=True)


@router.callback_query(F.data == callback_data['admin']['general']['add'] + "_programs")
async def process_admins_add_program_photo(clb_query: CallbackQuery, state: FSMContext) -> None:
    await admins_programs_controller.admins_add_program_photo(msg=clb_query.message, state=state)


@router.message(StateFilter(CreateProgramState.photo), F.photo)
async def process_admins_add_program_title(msg: Message, state: FSMContext) -> None:
    await admins_programs_controller.admins_add_program_title(msg=msg, state=state)


@router.message(StateFilter(CreateProgramState.title), F.text)
async def process_admins_add_program_description(msg: Message, state: FSMContext) -> None:
    await admins_programs_controller.admins_add_program_description(msg=msg, state=state)


@router.message(StateFilter(CreateProgramState.description), F.text)
async def process_admins_add_program_link(msg: Message, state: FSMContext) -> None:
    await admins_programs_controller.admins_add_program_link(msg=msg, state=state)


@router.message(StateFilter(CreateProgramState.link), F.text)
async def process_admins_add_program_finish(msg: Message, state: FSMContext) -> None:
    await admins_programs_controller.admins_add_program_finish(msg=msg, state=state)


@router.callback_query(F.data == callback_data['admin']['general']['delete'] + "_programs")
async def process_admins_delete_program(clb_query: CallbackQuery) -> None:
    program_id = str(clb_query.data.split("-")[1])

    await admins_programs_controller.admins_delete_program(msg=clb_query.message, program_id=program_id)


@router.callback_query(lambda query: query.data.startswith(
    callback_data['admin']['general']['edit']['main'] + "_programs"
))
async def process_admins_edit_program(clb_query: CallbackQuery, state: FSMContext) -> None:
    program_id = str(clb_query.data.split("-")[1])

    await admins_programs_controller.admins_edit_program(msg=clb_query.message,
                                                         state=state,
                                                         program_id=program_id)


@router.callback_query(lambda query: any(
    edit_action in query.data for edit_action in [
        callback_data['admin']['general']['edit']['photo'] + "_programs",
        callback_data['admin']['general']['edit']['title'] + "_programs",
        callback_data['admin']['general']['edit']['description'] + "_programs",
        callback_data['admin']['general']['edit']['link'] + "_programs",
        callback_data['admin']['general']['edit']['activity'] + "_programs"
    ]
))
async def process_admins_edit_program_property(clb_query: CallbackQuery, state: FSMContext) -> None:
    property = str(clb_query.data.split("_")[2])

    await admins_programs_controller.admins_edit_program_property(msg=clb_query.message, state=state, property=property)


@router.message(StateFilter(
    EditProgramState.value
), F.photo | F.text)
async def process_admins_edit_program_value(msg: Message, state: FSMContext) -> None:
    await admins_programs_controller.admins_edit_program_value(msg=msg, state=state)
