from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.admins.events.admins_events_controller import AdminsEventsController
from src.admins.states.events.create_event_state import CreateEventState
from src.admins.states.events.edit_event_state import EditEventState
from src.middlewares.admins_middleware import AdminsMiddleware
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()
router.message.middleware(AdminsMiddleware())

admins_events_controller: AdminsEventsController = AdminsEventsController()

lexicon = load_lexicon()
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")


@router.message(F.text == buttons["admin"]["main_panel"]["events"])
async def process_admins_get_events(msg: Message) -> None:
    await admins_events_controller.admins_get_events(msg)


@router.callback_query(lambda query: query.data.startswith("admins_pagen_next_events"))
async def process_admins_pagen_next_events(clb_query: CallbackQuery) -> None:
    offset_split = str(clb_query.data.split("-")[1])

    offset = int(offset_split) + 1

    await admins_events_controller.admins_get_events(msg=clb_query.message,
                                                     offset=offset,
                                                     edit=True)


@router.callback_query(lambda query: query.data.startswith("admins_pagen_backward_events"))
async def process_admins_pagen_backward_events(clb_query: CallbackQuery) -> None:
    offset_split = str(clb_query.data.split("-")[1])
    offset = int(offset_split) - 1

    await admins_events_controller.admins_get_events(msg=clb_query.message,
                                                     offset=offset,
                                                     edit=True)


@router.callback_query(F.data == callback_data['admin']['general']['add'] + "_events")
async def process_admins_add_event_photo(clb_query: CallbackQuery, state: FSMContext) -> None:
    await admins_events_controller.admins_add_event_photo(msg=clb_query.message, state=state)


@router.message(StateFilter(CreateEventState.photo), F.photo)
async def process_admins_add_event_title(msg: Message, state: FSMContext) -> None:
    await admins_events_controller.admins_add_event_title(msg=msg, state=state)


@router.message(StateFilter(CreateEventState.title), F.text)
async def process_admins_add_event_description(msg: Message, state: FSMContext) -> None:
    await admins_events_controller.admins_add_event_description(msg=msg, state=state)


@router.message(StateFilter(CreateEventState.description), F.text)
async def process_admins_add_event_event_date(msg: Message, state: FSMContext) -> None:
    await admins_events_controller.admins_add_event_date(msg=msg, state=state)


@router.message(StateFilter(CreateEventState.event_date), F.text)
async def process_admins_add_event_event_link(msg: Message, state: FSMContext) -> None:
    await admins_events_controller.admins_add_event_link(msg=msg, state=state)


@router.message(StateFilter(CreateEventState.link), F.text)
async def process_admins_add_event_event_link(msg: Message, state: FSMContext) -> None:
    await admins_events_controller.admins_add_event_finish(msg=msg, state=state)


@router.callback_query(lambda query: any(
    edit_action in query.data for edit_action in [
        callback_data['admin']['general']['delete'] + "_events",
    ]
))
async def process_admins_delete_event(clb_query: CallbackQuery) -> None:
    event_id = str(clb_query.data.split("-")[1])

    await admins_events_controller.admins_delete_event(msg=clb_query.message, event_id=event_id)


@router.callback_query(lambda query: query.data.startswith(
    callback_data['admin']['general']['edit']['main'] + "_events"
))
async def process_admins_edit_event(clb_query: CallbackQuery, state: FSMContext) -> None:
    event_id = str(clb_query.data.split("-")[1])

    await admins_events_controller.admins_edit_event(msg=clb_query.message,
                                                     state=state,
                                                     event_id=event_id)


@router.callback_query(lambda query: any(
    edit_action in query.data for edit_action in [
        callback_data['admin']['general']['edit']['photo'] + "_events",
        callback_data['admin']['general']['edit']['title'] + "_events",
        callback_data['admin']['general']['edit']['description'] + "_events",
        callback_data['admin']['general']['edit']['date'] + "_events",
        callback_data['admin']['general']['edit']['link'] + "_events",
        callback_data['admin']['general']['edit']['activity'] + "_events"
    ]
))
async def process_admins_edit_event_property(clb_query: CallbackQuery, state: FSMContext) -> None:
    property = str(clb_query.data.split("_")[2])

    await admins_events_controller.admins_edit_event_property(msg=clb_query.message, state=state, property=property)


@router.message(StateFilter(
    EditEventState.value
), F.photo | F.text)
async def process_admins_edit_event_value(msg: Message, state: FSMContext) -> None:
    await admins_events_controller.admins_edit_event_value(msg=msg, state=state)
