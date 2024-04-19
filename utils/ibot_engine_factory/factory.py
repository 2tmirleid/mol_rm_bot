from aiogram import Bot, Dispatcher

from utils.logger import Logger
from utils.watcher import Watcher


class IBotEngineFactory:
    def __init__(self,
                 token: str,
                 routers: list,
                 ) -> None:
        self.token = token
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(bot=self.bot)

        self.logger = Logger()
        self.watcher = Watcher()

        self.routers = routers

    async def launch(self):
        if self.routers is not None:
            for router in self.routers:
                self.dp.include_router(router)

        self.logger.log()
        self.watcher.watch()

        await self.dp.start_polling(self.bot)
