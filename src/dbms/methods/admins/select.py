class Select:
    def __init__(self):
        ...

    async def get_admin_by_chat_id(self, chat_id: str) -> str:
        return f"""SELECT """