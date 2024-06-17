from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.admins.events.admins_events_controller import AdminsEventsController
from src.admins.states.events.create_event_state import CreateEventState
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
