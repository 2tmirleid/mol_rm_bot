from src.dbms.connection import cursor, conn
from src.dbms.methods.admins.select_from_admins import SelectFromAdmins


class AdminsProgramsService:
    def __init__(self):
        self.cursor: cursor = cursor
        self.conn: conn = conn

        self.select: SelectFromAdmins = SelectFromAdmins()

    async def get_all_programs(self, offset=0) -> list:
        try:
            self.cursor.execute(
                await self.select.select_all_programs(offset=offset)
            )

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error while get all programs from db: {e}")

    async def get_programs_count(self) -> list:
        try:
            self.cursor.execute(
                await self.select.select_programs_count()
            )

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error while get count of programs: {e}")
