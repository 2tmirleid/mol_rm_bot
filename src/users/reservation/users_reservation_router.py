from aiogram import Router, F
from aiogram.types import Message

from src.users.reservation.users_reservation_controller import UsersReservationController
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

lexicon = load_lexicon()
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")
replicas = lexicon.get("replicas")

users_reservation_controller: UsersReservationController = UsersReservationController()


@router.message(F.text == buttons['users']['main_panel']['reservation'])
async def process_users_reservation_redirect(msg: Message) -> None:
    await users_reservation_controller.users_reservation_redirect(msg=msg)
