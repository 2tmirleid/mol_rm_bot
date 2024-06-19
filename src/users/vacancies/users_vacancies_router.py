from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from src.users.vacancies.users_vacancies_controller import UsersVacanciesController
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

lexicon = load_lexicon()
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")

users_vacancies_controller: UsersVacanciesController = UsersVacanciesController()


@router.message(F.text == buttons['users']['main_panel']['vacancies'])
async def process_users_get_active_vacancies(msg: Message) -> None:
    await users_vacancies_controller.users_get_active_vacancies(msg)


@router.message(F.text == buttons['users']['vacancies']['take_part'])
async def process_users_take_part_vacancies(msg: Message) -> None:
    await users_vacancies_controller.users_take_part_vacancies(msg=msg)


@router.message(F.text == buttons['users']['vacancies']['partners'])
async def process_users_get_partners_vacancies(msg: Message) -> None:
    await users_vacancies_controller.users_get_partners_vacancies(msg=msg)


@router.callback_query(lambda query: query.data.startswith("users_pagen_next_vacancies"))
async def process_users_pagen_next_vacancies(clb_query: CallbackQuery) -> None:
    offset_split = str(clb_query.data.split("-")[1])

    offset = int(offset_split) + 1

    await users_vacancies_controller.users_get_active_vacancies(msg=clb_query.message,
                                                                offset=offset,
                                                                edit=True)


@router.callback_query(lambda query: query.data.startswith("users_pagen_backward_vacancies"))
async def process_users_pagen_backward_vacancies(clb_query: CallbackQuery) -> None:
    offset_split = str(clb_query.data.split("-")[1])
    offset = int(offset_split) - 1

    await users_vacancies_controller.users_get_active_vacancies(msg=clb_query.message,
                                                                offset=offset,
                                                                edit=True)
