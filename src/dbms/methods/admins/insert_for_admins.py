from typing import Tuple, Any


class InsertForAdmins:
    def __init__(self):
        ...

    async def insert_program(self, program: list) -> str:
        return f"""INSERT INTO programs (photo, title, description, link)
        VALUES ('{program[0]}', '{program[1]}', '{program[2]}', '{program[3]}')"""

    async def insert_event(self, event: list) -> str:
        return f"""INSERT INTO events (photo, title, description, event_date, link)
        VALUES ('{event[0]}', '{event[1]}', '{event[2]}', '{event[3]}', '{event[4]}')"""
