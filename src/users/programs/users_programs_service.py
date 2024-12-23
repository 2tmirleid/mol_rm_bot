from psycopg2.extras import DictCursor

from src.dbms.connection import cursor, conn
from src.dbms.methods.users.select_for_users import SelectForUsers


class UsersProgramsService:
    def __init__(self):
        self.cursor: cursor = cursor
        self.conn: conn = conn

        self.select_for_users: SelectForUsers = SelectForUsers()

    # Пробный фикс
    async def exec(self, query: str, fetch=False, commit=False):
        with self.conn.cursor(cursor_factory=DictCursor) as dict_cursor:
            dict_cursor.execute(query)

            if fetch:
                return dict_cursor.fetchall()
            if commit:
                return self.conn.commit()

    async def get_program_description(self) -> list:
        # self.conn.cursor.execute(
        #     await self.select_for_users.select_program_description()
        # )
        #
        # return self.cursor.fetchall()

        query = await self.select_for_users.select_program_description()

        return await self.exec(query=query, fetch=True)

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
