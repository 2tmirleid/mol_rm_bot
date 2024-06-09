import asyncio
import os

from dotenv import load_dotenv, find_dotenv

from src.admins.commands import admins_commands_router
from utils.ibot_engine_factory.factory import IBotEngineFactory

"""Main app class"""


class Main:
    def __init__(self):
        load_dotenv(find_dotenv())

        self.bot = IBotEngineFactory(token=os.environ["TOKEN"],
                                     routers=[
                                         admins_commands_router.router
                                     ],
                                     scenes=[])
    
    async def start(self):
        await self.bot.launch()


if __name__ == "__main__":
    main = Main()
    asyncio.run(main.start())
