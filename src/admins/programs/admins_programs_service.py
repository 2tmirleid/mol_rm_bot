from src.dbms.connection import conn
from src.dbms.methods.admins.delete_for_admins import DeleteForAdmins
from src.dbms.methods.admins.insert_for_admins import InsertForAdmins
from src.dbms.methods.admins.select_for_admins import SelectForAdmins
from src.dbms.methods.admins.update_for_admins import UpdateForAdmins


class AdminsProgramsService:
    def __init__(self):
        self.conn = conn
        self.select_for_admins = SelectForAdmins()
        self.insert_for_admins = InsertForAdmins()
        self.delete_for_admins = DeleteForAdmins()
        self.update_for_admins = UpdateForAdmins()

    async def update_program_description(self, description: str):
        try:
            async with self.conn.cursor() as cursor:
                await cursor.execute(
                    await self.update_for_admins.update_program_description(description)
                )
                self.conn.commit()
        except Exception as e:
            print(f"Error while updating program from db: {e}")

    async def get_program_description(self) -> list:
        try:
            async with self.conn.cursor() as cursor:
                await cursor.execute(
                    await self.select_for_admins.select_program_description()
                )
                return await cursor.fetchall()
        except Exception as e:
            print(f"Error while get program from db: {e}")

    async def get_all_programs(self, offset=0) -> list:
        try:
            async with self.conn.cursor() as cursor:
                await cursor.execute(
                    await self.select_for_admins.select_all_programs(offset=offset)
                )
                return await cursor.fetchall()
        except Exception as e:
            print(f"Error while get all programs from db: {e}")

    async def get_programs_count(self) -> list:
        try:
            async with self.conn.cursor() as cursor:
                await cursor.execute(
                    await self.select_for_admins.select_programs_count()
                )
                return await cursor.fetchall()
        except Exception as e:
            print(f"Error while get count of programs: {e}")

    async def add_program(self, program: list) -> bool:
        try:
            async with self.conn.cursor() as cursor:
                await cursor.execute(
                    await self.insert_for_admins.insert_program(program=program)
                )
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Error while add of program: {e}")
            return False

    async def delete_program(self, program_id: str) -> bool:
        try:
            async with self.conn.cursor() as cursor:
                await cursor.execute(
                    await self.delete_for_admins.delete_program(program_id=program_id)
                )
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Error while deleting program: {e}")
            return False

    async def change_program_activity(self, program_id: str) -> bool:
        try:
            program_activity = await self.get_program_activity_by_id(program_id=program_id)

            async with self.conn.cursor() as cursor:
                await cursor.execute(
                    await self.update_for_admins.update_program_activity(
                        program_id=program_id, program_activity=program_activity[0][0]
                    )
                )
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Error while change program activity: {e}")
            return False

    async def get_program_activity_by_id(self, program_id):
        try:
            async with self.conn.cursor() as cursor:
                await cursor.execute(
                    await self.select_for_admins.select_program_activity_by_id(program_id=program_id)
                )
                return await cursor.fetchall()
        except Exception as e:
            print(f"Error while get program activity by id: {e}")
            return False

    async def edit_program(self, program_id: str, property: str, value: str) -> bool:
        try:
            async with self.conn.cursor() as cursor:
                await cursor.execute(
                    await self.update_for_admins.update_program(
                        program_id=program_id, property=property, value=value
                    )
                )
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Error while update program: {e}")
            return False

