from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from src.users.contacts.users_contacts_controller import UsersContactsController
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

lexicon = load_lexicon()
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")

users_contacts_controller: UsersContactsController = UsersContactsController()


@router.message(F.text == buttons['users']['main_panel']['contacts'])
async def process_users_get_contacts(msg: Message) -> None:
    await users_contacts_controller.users_get_contacts(msg=msg)


@router.message(F.photo)
async def test(msg: Message):
    await msg.answer(f'{msg.photo[-1].file_id}')


# @router.callback_query(lambda query: query.data.startswith("tel_"))
# async def process_users_get_contacts_phone(clb_query: CallbackQuery) -> None:
#     phone = str(clb_query.data.split("_")[1])
#
#     await users_contacts_controller.users_get_contacts_phone(msg=clb_query.message, phone=phone)
#
#
# @router.message(F.text == buttons['users']['contacts']['ask'])
# async def process_users_ask_question(msg: Message) -> None:
#     await users_contacts_controller.users_ask_question(msg=msg)
#
#
# @router.callback_query(lambda query: query.data.startswith("users_pagen_next_contacts"))
# async def process_users_pagen_next_contacts(clb_query: CallbackQuery) -> None:
#     offset_split = str(clb_query.data.split("-")[1])
#
#     offset = int(offset_split) + 1
#
#     await users_contacts_controller.users_get_contacts(msg=clb_query.message,
#                                                        offset=offset,
#                                                        edit=True)
#
#
# @router.callback_query(lambda query: query.data.startswith("users_pagen_backward_contacts"))
# async def process_users_pagen_backward_contacts(clb_query: CallbackQuery) -> None:
#     offset_split = str(clb_query.data.split("-")[1])
#     offset = int(offset_split) - 1
#
#     await users_contacts_controller.users_get_contacts(msg=clb_query.message,
#                                                        offset=offset,
#                                                        edit=True)
