from aiogram import Router, F
from aiogram.types import Message

from src.middlewares.admins_middleware import AdminsMiddleware
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()
router.message.middleware(AdminsMiddleware())

lexicon = load_lexicon()
buttons = lexicon.get("buttons")


@router.message(F.text == buttons["admin"]["main_panel"]["programs"])
async def process_admins_get_programs(msg: Message) -> None:
    ...
