import time


class IBotEngineDateFormatter:
    def __init__(self):
        self.date_format = "%Y-%m-%d %H:%M:%S"
        self.current_time = time.localtime()
        self.formatted_date = time.strftime(self.date_format, self.current_time)

    async def get_date(self):
        return str(self.formatted_date)
