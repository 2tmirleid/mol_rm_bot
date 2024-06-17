from src.dbms.connection import cursor, conn
from src.dbms.methods.admins.delete_for_admins import DeleteForAdmins
from src.dbms.methods.admins.insert_for_admins import InsertForAdmins
from src.dbms.methods.admins.select_for_admins import SelectForAdmins
from src.dbms.methods.admins.update_for_admins import UpdateForAdmins


class AdminsVacanciesService:
    def __init__(self):
        self.cursor: cursor = cursor
        self.conn: conn = conn

        self.select_for_admins: SelectForAdmins = SelectForAdmins()
        self.insert_for_admins: InsertForAdmins = InsertForAdmins()
        self.delete_for_admins: DeleteForAdmins = DeleteForAdmins()
        self.update_for_admins: UpdateForAdmins = UpdateForAdmins()

    async def get_all_vacancies(self, offset=0) -> list:
        try:
            self.cursor.execute(
                await self.select_for_admins.select_all_vacancies(offset=offset)
            )

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error while get all vacancies from db: {e}")

    async def get_vacancies_count(self) -> list:
        try:
            self.cursor.execute(
                await self.select_for_admins.select_vacancies_count()
            )

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error while get count of vacancies: {e}")

    async def add_vacancy(self, vacancy: list) -> bool:
        try:
            self.cursor.execute(
                await self.insert_for_admins.insert_vacancy(vacancy=vacancy)
            )
            self.conn.commit()

            return True
        except Exception as e:
            print(f"Error while add of vacancy: {e}")
            return False

    async def delete_vacancy(self, vacancy_id: str) -> bool:
        try:
            self.cursor.execute(
                await self.delete_for_admins.delete_vacancy(vacancy_id=vacancy_id)
            )

            self.conn.commit()

            return True
        except Exception as e:
            print(f"Error while deleting vacancy: {e}")
            return False
