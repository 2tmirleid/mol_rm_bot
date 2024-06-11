from src.dbms.connection import cursor, conn
from src.dbms.methods.admins.select_from_admins import SelectFromAdmins


class MainAdminsService:
    def __init__(self):
        self.cursor: cursor = cursor
        self.conn: conn = conn

        self.select: SelectFromAdmins = SelectFromAdmins()

    async def get_admin_by_username(self, username: str) -> list:
        try:
            self.cursor.execute(
                await self.select.select_admin_by_username(username)
            )

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error while getting admin by username: {e}")

    async def get_admin_by_chat_id(self, chat_id: str) -> list:
        try:
            self.cursor.execute(
                await self.select.select_admin_by_chat_id(chat_id)
            )

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error while getting admin by username: {e}")