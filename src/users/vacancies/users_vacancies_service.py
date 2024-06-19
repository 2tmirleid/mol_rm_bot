from src.dbms.connection import cursor, conn
from src.dbms.methods.users.select_for_users import SelectForUsers


class UsersVacanciesService:
    def __init__(self):
        self.cursor: cursor = cursor
        self.conn: conn = conn

        self.select_for_users: SelectForUsers = SelectForUsers()

    async def get_active_vacancies(self, offset=0) -> list:
        try:
            self.cursor.execute(
                await self.select_for_users.select_active_vacancies(offset=offset)
            )

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error while get active vacancies from db: {e}")

    async def get_active_vacancies_count(self) -> list:
        try:
            self.cursor.execute(
                await self.select_for_users.select_vacancies_count()
            )

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error while get count of vacancies: {e}")