class Select:
    def __init__(self):
        ...

    async def select_admin_by_username(self, username: str) -> str:
        return f"""SELECT _id FROM admins WHERE telegram_username = '{username}'"""

    async def select_admin_by_chat_id(self, chat_id: str) -> str:
        return f"""SELECT _id FROM admins WHERE telegram_chat_id = '{chat_id}'"""
