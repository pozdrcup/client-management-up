import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            if query.strip().upper().startswith("SELECT"):
                return self.cursor.fetchall()
            else:
                self.conn.commit()
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            self.conn.rollback()

    def close(self):
        self.cursor.close()
        self.conn.close()
