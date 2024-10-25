from src.dbms.connection import cursor, conn
from src.dbms.methods.admins.delete_for_admins import DeleteForAdmins
from src.dbms.methods.admins.insert_for_admins import InsertForAdmins
from src.dbms.methods.admins.select_for_admins import SelectForAdmins
from src.dbms.methods.admins.update_for_admins import UpdateForAdmins


class MainAdminsService:
    def __init__(self):
        self.cursor: cursor = cursor
        self.conn: conn = conn

        self.select_for_admins: SelectForAdmins = SelectForAdmins()
        self.insert_for_admins: InsertForAdmins = InsertForAdmins()
        self.delete_for_admins: DeleteForAdmins = DeleteForAdmins()
        self.update_for_admins: UpdateForAdmins = UpdateForAdmins()

    async def get_admin_by_username(self, username: str) -> list:
        try:
            self.cursor.execute(
                await self.select_for_admins.select_admin_by_username(username)
            )

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error while getting admin by username: {e}")

    async def get_admin_by_chat_id(self, chat_id: str) -> list:
        try:
            self.cursor.execute(
                await self.select_for_admins.select_admin_by_chat_id(chat_id)
            )

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error while getting admin by username: {e}")

    async def get_all_admins(self, offset=0) -> list:
        try:
            self.cursor.execute(
                await self.select_for_admins.select_all_admins(offset=offset)
            )

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error while get all admins from db: {e}")

    async def get_admins_count(self) -> list:
        try:
            self.cursor.execute(
                await self.select_for_admins.select_admins_count()
            )

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error while get count of admins: {e}")

    async def add_admin(self, admin: list) -> bool:
        try:
            self.cursor.execute(
                await self.insert_for_admins.insert_admin(admin=admin)
            )
            self.conn.commit()

            return True
        except Exception as e:
            print(f"Error while add of admin: {e}")
            return False

    async def delete_admin(self, admin_id: str) -> bool:
        try:
            self.cursor.execute(
                await self.delete_for_admins.delete_admin(admin_id=admin_id)
            )

            self.conn.commit()

            return True
        except Exception as e:
            print(f"Error while deleting admin: {e}")
            return False

    async def edit_admin(self, admin_id: str, property: str, value: str) -> bool:
        try:
            self.cursor.execute(
                await self.update_for_admins.update_admin(admin_id=admin_id, property=property, value=value)
            )

            self.conn.commit()

            return True
        except Exception as e:
            print(f"Error while update admin: {e}")
            return False
