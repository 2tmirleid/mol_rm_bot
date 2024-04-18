import logging


class Logger:
    def __init__(self):
        ...

    def log(self):
        logging.basicConfig(
            format='[IBotEngine] - %(asctime)s - %(message)s',
            datefmt='[%Y-%m-%d %H:%M:%S]',
            level=logging.INFO
        )
        logging.getLogger("httpx").setLevel(logging.WARNING)
