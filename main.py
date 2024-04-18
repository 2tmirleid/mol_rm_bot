import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv, find_dotenv

from src.example_dir import example_router
from utils.logger import Logger
from utils.watcher import Watcher

"""Main app class"""


class Main:
    def __init__(self):
        load_dotenv(find_dotenv())

        self.token  = os.environ['TOKEN']
        self.bot    = Bot(token=self.token)
        self.dp     = Dispatcher(bot=self.bot)

        self.logger = Logger()
        self.watcher = Watcher()

    # Method for getting app routers
    def get_routers(self):
        self.dp.include_router(example_router.router)

    def start(self):
        # Init logging
        self.logger.log()

        # Watch for changes in project
        self.watcher.watch()

        # Get routers
        self.get_routers()

        # Start polling
        self.dp.run_polling(self.bot)


if __name__ == "__main__":
    main = Main()
    main.start()