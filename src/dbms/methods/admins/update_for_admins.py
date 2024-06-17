


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

