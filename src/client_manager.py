from src.db import DatabaseManager
from src.models import Client

class ClientManager:
    def __init__(self):
        self.db = DatabaseManager()

    def add_client(self, client: Client):
        query = """
        INSERT INTO clients (full_name, contact_info, registration_date, notes)
        VALUES (%s, %s, %s, %s)
        """
        params = (client.full_name, client.contact_info, client.registration_date, client.notes)
        self.db.execute_query(query, params)

    def get_all_clients(self):
        query = "SELECT * FROM clients ORDER BY registration_date DESC"
        return self.db.execute_query(query)

    def search_clients(self, search_term):
        query = """
        SELECT * FROM clients
        WHERE full_name ILIKE %s OR contact_info ILIKE %s OR notes ILIKE %s
        """
        params = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
        return self.db.execute_query(query, params)

    def update_client(self, client_id, client: Client):
        query = """
        UPDATE clients SET full_name=%s, contact_info=%s, registration_date=%s, notes=%s
        WHERE id=%s
        """
        params = (client.full_name, client.contact_info, client.registration_date, client.notes, client_id)
        self.db.execute_query(query, params)

    def delete_client(self, client_id):
        query = "DELETE FROM clients WHERE id=%s"
        params = (client_id,)
        self.db.execute_query(query, params)

    def close(self):
        self.db.close()
