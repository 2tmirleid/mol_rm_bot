from datetime import datetime, timedelta

from src.dbms.connection import cursor, conn
from src.dbms.methods.users.select_for_users import SelectForUsers


class UsersEventsService:
    def __init__(self):
        self.cursor: cursor = cursor
        self.conn: conn = conn

        self.select_for_users: SelectForUsers = SelectForUsers()

    async def get_active_events(self, offset=0) -> list:
        try:
            today = datetime.now()
            first_day = today.strftime("%Y-%m-%d")

            last_week = today + timedelta(days=14)
            last_week_day = last_week.strftime("%Y-%m-%d")

            self.cursor.execute(
                await self.select_for_users.select_active_events(
                    offset=offset, first_day=first_day, last_week_day=last_week_day
                )
            )

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error while get active events from db: {e}")

    async def get_active_events_count(self) -> list:
        try:
            today = datetime.now()
            first_day = today.strftime("%Y-%m-%d")

            last_week = today + timedelta(days=14)
            last_week_day = last_week.strftime("%Y-%m-%d")

            self.cursor.execute(
                await self.select_for_users.select_events_count(first_day=first_day, last_week_day=last_week_day)
            )

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error while get count of events: {e}")