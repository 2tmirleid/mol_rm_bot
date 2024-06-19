class SelectForUsers:
    def __init__(self):
        ...

    async def select_active_programs(self, offset=0) -> str:
        return f"""SELECT photo, title, description, link FROM programs WHERE is_active = TRUE ORDER BY _id ASC LIMIT 1 OFFSET {offset}"""\

    async def select_programs_count(self) -> str:
        return """SELECT COUNT(*) FROM programs WHERE is_active = TRUE"""
