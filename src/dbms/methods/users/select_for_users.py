class SelectForUsers:
    def __init__(self):
        ...

    async def select_active_programs(self, offset=0) -> str:
        return f"""SELECT photo, title, description, link FROM programs WHERE is_active = TRUE ORDER BY _id ASC LIMIT 1 OFFSET {offset}"""\

    async def select_programs_count(self) -> str:
        return """SELECT COUNT(*) FROM programs WHERE is_active = TRUE"""

    async def select_active_vacancies(self, offset=0) -> str:
        return f"""SELECT photo, title, description, link FROM vacancies WHERE is_active = TRUE ORDER BY _id ASC LIMIT 1 OFFSET {offset}"""\

    async def select_vacancies_count(self) -> str:
        return """SELECT COUNT(*) FROM vacancies WHERE is_active = TRUE"""

    async def select_active_events(self, first_day, last_week_day, offset=0, ) -> str:
        return f"""SELECT photo, title, description, date, link FROM events WHERE is_active = TRUE AND date >= '{first_day}' AND date <= '{last_week_day}' ORDER BY _id ASC LIMIT 1 OFFSET {offset}"""\

    async def select_events_count(self, first_day, last_week_day) -> str:
        return f"""SELECT COUNT(*) FROM events WHERE is_active = TRUE AND date >= '{first_day}' AND date <= '{last_week_day}'"""

    async def select_contacts(self, offset=0) -> str:
        return f"""SELECT photo, name, description, phone FROM admins ORDER BY _id ASC LIMIT 1 OFFSET {offset}"""\

    async def select_contacts_count(self) -> str:
        return """SELECT COUNT(*) FROM admins"""
