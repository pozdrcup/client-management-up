# src/db.py
import psycopg2
from psycopg2.extras import RealDictCursor

class DatabaseManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="client_db",
            user="postgres",
            password= 9156  # ← ОБЯЗАТЕЛЬНО укажите!
        )
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
)



