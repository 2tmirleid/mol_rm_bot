from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from src.users.events.users_events_controller import UsersEventsController
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

lexicon = load_lexicon()
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")

users_events_controller: UsersEventsController = UsersEventsController()


@router.message(F.text == buttons['users']['main_panel']['events'])
async def process_users_get_active_events(msg: Message) -> None:
    await users_events_controller.users_get_active_events(msg=msg)


@router.message(F.text == buttons['users']['events']['calendar'])
async def process_users_get_calendar_events(msg: Message) -> None:
    await users_events_controller.users_get_calendar_events(msg=msg)


@router.callback_query(lambda query: query.data.startswith("users_pagen_next_events"))
async def process_users_pagen_next_events(clb_query: CallbackQuery) -> None:
    offset_split = str(clb_query.data.split("-")[1])

    offset = int(offset_split) + 1

    await users_events_controller.users_get_active_events(msg=clb_query.message,
                                                          offset=offset,
                                                          edit=True)


@router.callback_query(lambda query: query.data.startswith("users_pagen_backward_events"))
async def process_users_pagen_backward_events(clb_query: CallbackQuery) -> None:
    offset_split = str(clb_query.data.split("-")[1])
    offset = int(offset_split) - 1

    await users_events_controller.users_get_active_events(msg=clb_query.message,
                                                          offset=offset,
                                                          edit=True)
