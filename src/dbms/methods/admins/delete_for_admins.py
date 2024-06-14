class DeleteForAdmins:
    def __init__(self):
        ...

    async def delete_program(self, program_id: str) -> str:
        return f"""DELETE FROM programs WHERE _id = '{program_id}'"""