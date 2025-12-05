from src.db import DatabaseManager
from src.models import Order

class OrderManager:
    def __init__(self):
        self.db = DatabaseManager()

    def add_order(self, order: Order):
        query = """
        INSERT INTO orders (client_id, order_date, description, amount)
        VALUES (%s, %s, %s, %s)
        """
        params = (order.client_id, order.order_date, order.description, order.amount)
        self.db.execute_query(query, params)

    def get_orders_by_client(self, client_id):
        query = """
        SELECT id, client_id, order_date, description, amount
        FROM orders
        WHERE client_id = %s
        ORDER BY order_date DESC
        """
        return self.db.execute_query(query, (client_id,))

    def get_all_orders(self):
        query = """
        SELECT id, client_id, order_date, description, amount
        FROM orders
        ORDER BY order_date DESC
        """
        return self.db.execute_query(query)

    def search_orders(self, search_term):
        query = """
        SELECT o.id, o.client_id, o.order_date, o.description, o.amount, c.full_name AS client_name
        FROM orders o
        JOIN clients c ON o.client_id = c.id
        WHERE c.full_name ILIKE %s OR o.description ILIKE %s
        ORDER BY o.order_date DESC
        """
        params = (f"%{search_term}%", f"%{search_term}%")
        return self.db.execute_query(query, params)

    def update_order(self, order_id, order: Order):
        query = """
        UPDATE orders
        SET client_id = %s, order_date = %s, description = %s, amount = %s
        WHERE id = %s
        """
        params = (order.client_id, order.order_date, order.description, order.amount, order_id)
        self.db.execute_query(query, params)

    def delete_order(self, order_id):
        query = "DELETE FROM orders WHERE id = %s"
        self.db.execute_query(query, (order_id,))

    def close(self):
        self.db.close()
