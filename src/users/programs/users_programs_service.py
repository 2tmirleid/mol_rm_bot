from src.dbms.connection import cursor, conn
from src.dbms.methods.users.select_for_users import SelectForUsers


class UsersProgramsService:
    def __init__(self):
        self.cursor: cursor = cursor
        self.conn: conn = conn

        self.select_for_users: SelectForUsers = SelectForUsers()

    async def get_program_description(self) -> list:
        self.cursor.execute(
            await self.select_for_users.select_program_description()
        )

        return self.cursor.fetchall()

    async def get_active_programs(self, offset=0) -> list:
        try:
            self.cursor.execute(
                await self.select_for_users.select_active_programs(offset=offset)
            )

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error while get active programs from db: {e}")

    async def get_active_programs_count(self) -> list:
        try:
            self.cursor.execute(
                await self.select_for_users.select_programs_count()
            )

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error while get count of programs: {e}")
