import time

from aiogram import Bot, Dispatcher

from aiogram.fsm.storage.memory import MemoryStorage

from utils.logger import Logger
from utils.watcher import Watcher


class IBotEngineFactory:
    def __init__(self,
                 token: str,
                 routers: list = None,
                 scenes: list = None) -> None:
        self.date_format = "%Y-%m-%d %H:%M:%S"
        self.current_time = time.localtime()
        self.formatted_date = time.strftime(self.date_format, self.current_time)

        self.storage = MemoryStorage()

        self.token = token
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(bot=self.bot)

        self.logger = Logger()
        self.watcher = Watcher()

        self.routers: list = routers if routers else []
        self.scenes: list = scenes if scenes else []

    async def launch(self):
        if self.routers:
            for router in self.routers:
                self.dp.include_router(router)
            print(f"[IBotEngine] - [{self.formatted_date}] - Initialized routers")

        if self.scenes:
            for scene in self.scenes:
                self.dp.include_router(scene)
            print(f"[IBotEngine] - [{self.formatted_date}] - Initialized scenes")

        self.logger.log()
        self.watcher.watch()

        await self.dp.start_polling(self.bot)
