import logging
import os
import sys

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer

from src.example_dir import example_router

"""Main app class"""


class Main:
    def __init__(self):
        load_dotenv()

        self.token = os.environ['TOKEN']
        self.bot   = Bot(token=self.token)
        self.dp    = Dispatcher(bot=self.bot)

    # Method for getting app routers
    def get_routers(self):
        self.dp.include_router(example_router.router)

    def start(self):
        # Init logging
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.INFO
        )
        logging.getLogger("httpx").setLevel(logging.WARNING)

        path = sys.argv[1] if len(sys.argv) > 1 else '.'

        event_handler = LoggingEventHandler()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        # Get routers
        self.get_routers()

        # Start polling
        self.dp.run_polling(self.bot)


if __name__ == "__main__":
    main = Main()
    main.start()