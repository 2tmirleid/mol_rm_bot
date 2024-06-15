import asyncio
import os

from dotenv import load_dotenv, find_dotenv

from src.admins import main_admins_router
from src.admins.events import admins_events_router
from src.admins.programs import admins_programs_router
from src.dbms.models.admins import create_admins_model
from src.dbms.models.events import create_events_model
from src.dbms.models.programs import create_programs_model
from src.dbms.models.vacancies import create_vacancies_model
from utils.ibot_engine_factory.factory import IBotEngineFactory

"""Main app class"""


class Main:
    def __init__(self):
        load_dotenv(find_dotenv())

        self.bot = IBotEngineFactory(token=os.environ["TOKEN"],
                                     routers=[
                                         main_admins_router.router,
                                         admins_programs_router.router,
                                         admins_events_router.router
                                     ],
                                     models=[
                                         create_admins_model,
                                         create_events_model,
                                         create_programs_model,
                                         create_vacancies_model
                                     ])
    
    async def start(self):
        await self.bot.launch()


if __name__ == "__main__":
    main = Main()
    asyncio.run(main.start())
