from src.dbms.connection import cursor, conn
from src.dbms.methods.admins.delete_for_admins import DeleteForAdmins
from src.dbms.methods.admins.insert_for_admins import InsertForAdmins
from src.dbms.methods.admins.select_for_admins import SelectForAdmins
from src.dbms.methods.admins.update_for_admins import UpdateForAdmins


class AdminsEventsService:
    def __init__(self):
        self.cursor: cursor = cursor
        self.conn: conn = conn

        self.select_for_admins: SelectForAdmins = SelectForAdmins()
        self.insert_for_admins: InsertForAdmins = InsertForAdmins()
        self.delete_for_admins: DeleteForAdmins = DeleteForAdmins()
        self.update_for_admins: UpdateForAdmins = UpdateForAdmins()

    async def get_all_events(self, offset=0) -> list:
        try:
            self.cursor.execute(
                await self.select_for_admins.select_all_events(offset=offset)
            )

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error while get all events from db: {e}")

    async def get_events_count(self) -> list:
        try:
            self.cursor.execute(
                await self.select_for_admins.select_events_count()
            )

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error while get count of events: {e}")

    async def add_event(self, event: list) -> bool:
        try:
            self.cursor.execute(
                await self.insert_for_admins.insert_event(event=event)
            )
            self.conn.commit()

            return True
        except Exception as e:
            print(f"Error while add of event: {e}")
            return False

    async def delete_event(self, event_id: str) -> bool:
        try:
            self.cursor.execute(
                await self.delete_for_admins.delete_event(event_id=event_id)
            )

            self.conn.commit()

            return True
        except Exception as e:
            print(f"Error while deleting event: {e}")
            return False

    async def change_event_activity(self, event_id: str) -> bool:
        try:
            event_activity = await self.get_event_activity_by_id(event_id=event_id)

            self.cursor.execute(
                await self.update_for_admins.update_event_activity(
                    event_id=event_id, event_activity=event_activity[0][0])
            )

            self.conn.commit()

            return True
        except Exception as e:
            print(f"Error while change event activity: {e}")
            return False

    async def get_event_activity_by_id(self, event_id):
        try:
            self.cursor.execute(
                await self.select_for_admins.select_event_activity_by_id(event_id=event_id)
            )

            event_activity = self.cursor.fetchall()

            return event_activity
        except Exception as e:
            print(f"Error while get event activity by id: {e}")
            return False

    async def edit_event(self, event_id: str, property: str, value: str) -> bool:
        try:
            self.cursor.execute(
                await self.update_for_admins.update_event(event_id=event_id, property=property, value=value)
            )

            self.conn.commit()

            return True
        except Exception as e:
            print(f"Error while update event: {e}")
            return False
