from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.admins.states.vacancies.create_vacancy_state import CreateVacancyState
from src.admins.vacancies.admins_vacancies_controller import AdminsVacanciesController
from src.middlewares.admins_middleware import AdminsMiddleware
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()
router.message.middleware(AdminsMiddleware())

admins_vacancies_controller: AdminsVacanciesController = AdminsVacanciesController()

lexicon = load_lexicon()
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")


@router.message(F.text == buttons["admin"]["main_panel"]["vacancies"])
async def process_admins_get_vacancies(msg: Message) -> None:
    await admins_vacancies_controller.admins_get_vacancies(msg)


@router.callback_query(lambda query: query.data.startswith("admins_pagen_next_vacancies"))
async def process_admins_pagen_next_vacancies(clb_query: CallbackQuery) -> None:
    offset_split = str(clb_query.data.split("-")[1])

    offset = int(offset_split) + 1

    await admins_vacancies_controller.admins_get_vacancies(msg=clb_query.message,
                                                           offset=offset,
                                                           edit=True)


@router.callback_query(lambda query: query.data.startswith("admins_pagen_backward_vacancies"))
async def process_admins_pagen_backward_vacancies(clb_query: CallbackQuery) -> None:
    offset_split = str(clb_query.data.split("-")[1])
    offset = int(offset_split) - 1

    await admins_vacancies_controller.admins_get_vacancies(msg=clb_query.message,
                                                           offset=offset,
                                                           edit=True)


@router.callback_query(F.data == callback_data['admin']['general']['add'] + "_vacancies")
async def process_admins_add_vacancy_photo(clb_query: CallbackQuery, state: FSMContext) -> None:
    await admins_vacancies_controller.admins_add_vacancy_photo(msg=clb_query.message, state=state)


@router.message(StateFilter(CreateVacancyState.photo), F.photo)
async def process_admins_add_vacancy_title(msg: Message, state: FSMContext) -> None:
    await admins_vacancies_controller.admins_add_vacancy_title(msg=msg, state=state)


@router.message(StateFilter(CreateVacancyState.title), F.text)
async def process_admins_add_vacancy_description(msg: Message, state: FSMContext) -> None:
    await admins_vacancies_controller.admins_add_vacancy_description(msg=msg, state=state)


@router.message(StateFilter(CreateVacancyState.description), F.text)
async def process_admins_add_vacancy_link(msg: Message, state: FSMContext) -> None:
    await admins_vacancies_controller.admins_add_vacancy_link(msg=msg, state=state)


@router.message(StateFilter(CreateVacancyState.link), F.text)
async def process_admins_add_program_finish(msg: Message, state: FSMContext) -> None:
    await admins_vacancies_controller.admins_add_vacancy_finish(msg=msg, state=state)


@router.callback_query(lambda query: any(
    edit_action in query.data for edit_action in [
        callback_data['admin']['general']['delete'] + "_vacancies",
    ]
))
async def process_admins_delete_vacancy(clb_query: CallbackQuery) -> None:
    vacancy_id = str(clb_query.data.split("-")[1])

    await admins_vacancies_controller.admins_delete_vacancy(msg=clb_query.message, vacancy_id=vacancy_id)
