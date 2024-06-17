class DeleteForAdmins:
    def __init__(self):
        ...

    async def delete_program(self, program_id: str) -> str:
        return f"""DELETE FROM programs WHERE _id = '{program_id}'"""

    async def delete_event(self, event_id: str) -> str:
        return f"""DELETE FROM events WHERE _id = '{event_id}'"""
