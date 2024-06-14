from typing import Tuple, Any


class InsertForAdmins:
    def __init__(self):
        ...

    async def insert_program(self, program: list) -> str:
        return f"""INSERT INTO programs (photo, title, description, link)
        VALUES ('{program[0]}', '{program[1]}', '{program[2]}', '{program[3]}')"""
