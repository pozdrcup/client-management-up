from datetime import date

class Client:
    def __init__(self, full_name, contact_info="", registration_date=None, notes=""):
        self.full_name = full_name
        self.contact_info = contact_info
        self.registration_date = registration_date or date.today()
        self.notes = notes

class Order:
    def __init__(self, client_id, order_date=None, description="", amount=0.0):
        self.client_id = client_id
        self.order_date = order_date or date.today()
        self.description = description
        self.amount = float(amount)
