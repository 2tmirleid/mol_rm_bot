class SelectForAdmins:
    def __init__(self):
        ...

    async def select_admin_by_username(self, username: str) -> str:
        return f"""SELECT _id FROM admins WHERE telegram_username = '{username}'"""

    async def select_admin_by_chat_id(self, chat_id: str) -> str:
        return f"""SELECT _id FROM admins WHERE telegram_chat_id = '{chat_id}'"""

    async def select_all_programs(self, offset=0) -> str:
        return f"""SELECT _id, photo, title, description, link, is_active FROM programs LIMIT 1 OFFSET {offset}"""

    async def select_programs_count(self) -> str:
        return """SELECT COUNT(*) FROM programs"""

    async def select_program_activity_by_id(self, program_id) -> str:
        return f"""SELECT is_active FROM programs WHERE _id = '{program_id}'"""

    async def select_all_events(self, offset=0) -> str:
        return f"""SELECT _id, photo, title, description, event_date, link, is_active FROM events LIMIT 1 OFFSET {offset}"""

    async def select_events_count(self) -> str:
        return """SELECT COUNT(*) FROM events"""