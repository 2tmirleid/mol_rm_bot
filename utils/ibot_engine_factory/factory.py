import time

from aiogram import Bot, Dispatcher

from aiogram.fsm.storage.memory import MemoryStorage

from utils.ibot_engine_factory.date.date_formatter import IBotEngineDateFormatter
from utils.ibot_engine_factory.orm.create_tables import create_tables
from utils.logger import Logger
from utils.watcher import Watcher


class IBotEngineFactory:
    def __init__(self,
                 token:       str,
                 routers:     list = None,
                 scenes:      list = None,
                 middlewares: list = None,
                 models:      list = None,
                 ) -> None:
        self.date_formatter: IBotEngineDateFormatter = IBotEngineDateFormatter()

        self.storage = MemoryStorage()

        self.token = token
        self.bot   = Bot(token=self.token)
        self.dp    = Dispatcher(bot=self.bot)

        self.logger  = Logger()
        self.watcher = Watcher()

        self.routers:     list = routers if routers else []
        self.scenes:      list = scenes if scenes else []
        self.middlewares: list = middlewares if middlewares else []
        self.models:      list = models if models else []

    async def launch(self):
        if self.routers:
            for router in self.routers:
                self.dp.include_router(router)
            print(f"[IBotEngine] - [{await self.date_formatter.get_date()}] - Initialized routers")

        if self.scenes:
            for scene in self.scenes:
                self.dp.include_router(scene)
            print(f"[IBotEngine] - [{await self.date_formatter.get_date()}] - Initialized scenes")

        if self.middlewares:
            for middleware in self.middlewares:
                self.dp.update.middleware(middleware)
            print(f"[IBotEngine] - [{await self.date_formatter.get_date()}] - Initialized middlewares")

        if self.models:
            for model in self.models:
                create_tables(model)
            print(f"[IBotEngine] - [{await self.date_formatter.get_date()}] - Initialized models")

        self.logger.log()
        self.watcher.watch()

        await self.dp.start_polling(self.bot)
