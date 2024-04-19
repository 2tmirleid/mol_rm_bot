from aiogram import Bot, Dispatcher

from aiogram.fsm.storage.memory import MemoryStorage

from utils.logger import Logger
from utils.watcher import Watcher


class IBotEngineFactory:
    def __init__(self,
                 token: str,
                 routers: list,
                 ) -> None:
        self.storage = MemoryStorage()

        self.token = token
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(bot=self.bot)

        self.logger = Logger()
        self.watcher = Watcher()

        self.routers: list = routers

    async def launch(self):
        if self.routers is not None:
            for router in self.routers:
                self.dp.include_router(router)

        self.logger.log()
        self.watcher.watch()

        await self.dp.start_polling(self.bot)
