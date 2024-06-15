from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from src.admins.events.admins_events_controller import AdminsEventsController
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
