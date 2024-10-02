
class UpdateForAdmins:
    def __init__(self):
        ...

    async def update_program_activity(self, program_activity: bool, program_id: str) -> str:
        return f"""UPDATE programs SET is_active = {not program_activity} WHERE _id = '{program_id}'"""

    async def update_program(self, program_id: str, property: str, value: str) -> str:
        return f"""UPDATE programs SET {property} = '{value}' WHERE _id = '{program_id}'"""

    async def update_event_activity(self, event_activity: bool, event_id: str) -> str:
        return f"""UPDATE events SET is_active = {not event_activity} WHERE _id = '{event_id}'"""

    async def update_event(self, event_id: str, property: str, value: str) -> str:
        return f"""UPDATE events SET {property} = '{value}' WHERE _id = '{event_id}'"""

    async def update_vacancy_activity(self, vacancy_activity: bool, vacancy_id: str) -> str:
        return f"""UPDATE vacancies SET is_active = {not vacancy_activity} WHERE _id = '{vacancy_id}'"""

    async def update_vacancy(self, vacancy_id: str, property: str, value: str) -> str:
        return f"""UPDATE vacancies SET {property} = '{value}' WHERE _id = '{vacancy_id}'"""

    async def update_admin(self, admin_id: str, property: str, value: str) -> str:
        return f"""UPDATE admins SET {property} = '{value}' WHERE _id = '{admin_id}'"""

    async def update_program_description(self, description: str) -> str:
        return f"""UPDATE programs SET description = '{description}'"""
