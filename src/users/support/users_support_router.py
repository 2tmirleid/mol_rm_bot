from aiogram import Router, F
from aiogram.types import Message

from src.users.support.users_support_controller import UsersSupportController
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

lexicon = load_lexicon()
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")

users_support_controller: UsersSupportController = UsersSupportController()


# @router.message(F.text == buttons['users']['main_panel']['support'])
# async def process_users_get_support_menu(msg: Message) -> None:
#     await users_support_controller.users_get_support_menu(msg)
#
#
# @router.message(F.text == buttons['users']['support']['team'])
# async def process_users_get_team_info(msg: Message) -> None:
#     await users_support_controller.users_get_team_info(msg)
#
#
# @router.message(F.text == buttons['users']['support']['contacts'])
# async def process_users_get_contacts_info(msg: Message) -> None:
#     await users_support_controller.users_get_contacts_info(msg)
#
#
# @router.message(F.text == buttons['users']['support']['part'])
# async def process_users_get_part_info(msg: Message) -> None:
#     await users_support_controller.users_get_part_info(msg)
#
#
# @router.message(F.text == buttons['users']['support']['schedule'])
# async def process_users_get_schedule_info(msg: Message) -> None:
#     await users_support_controller.users_get_schedule_info(msg)
#
#
# @router.message(F.text == buttons['users']['support']['places'])
# async def process_users_get_places_info(msg: Message) -> None:
#     await users_support_controller.users_get_places_info(msg)
#
#
# @router.message(F.text == buttons['users']['support']['rules'])
# async def process_users_get_rules_info(msg: Message) -> None:
#     await users_support_controller.users_get_rules_info(msg)
