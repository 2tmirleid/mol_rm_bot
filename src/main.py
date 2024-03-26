import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

"""Main app class"""


class Main:
    def __init__(self):
        load_dotenv()

        self.token = os.environ['TOKEN']
        self.bot   = Bot(token=self.token)
        self.dp    = Dispatcher(bot=self.bot)

    # Method for getting app routers
    def get_routers(self):
        ...

    def start(self):
        # Init logging
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        logging.getLogger("httpx").setLevel(logging.WARNING)

        # Get routers
        self.get_routers()

        # Start polling
        self.dp.run_polling(self.bot)


if __name__ == "__main__":
    main = Main()
    main.start()