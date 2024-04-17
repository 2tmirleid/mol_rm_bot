from src.dbms.connection import conn

"""THIS CLASS USING FOR MANIPULATIONS WITH DBMS"""


class ExampleService:
    def __init__(self):
        self.conn = conn
        self.cursor = self.conn.cursor()