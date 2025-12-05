# Добавьте в класс ExcelImporter или создайте ExcelExporter (лучше отдельно)

class ExcelExporter:
    def __init__(self):
        self.cm = ClientManager()
        self.om = OrderManager()

    def export_clients_to_excel(self, file_path: str):
        clients = self.cm.get_all_clients()
        if not clients:
            print("Нет клиентов для экспорта")
            return

        df = pd.DataFrame(clients, columns=[
            'ID', 'ФИО', 'Контактная информация', 'Дата регистрации', 'Примечания'
        ])
        df.to_excel(file_path, index=False)
        print(f"Экспортировано {len(clients)} клиентов → {file_path}")

    def export_orders_to_excel(self, file_path: str):
        orders = self.om.get_all_orders()
        if not orders:
            print("Нет заказов для экспорта")
            return

        df = pd.DataFrame(orders, columns=[
            'ID', 'ID клиента', 'Дата заказа', 'Описание', 'Сумма'
        ])
        df.to_excel(file_path, index=False)
        print(f"Экспортировано {len(orders)} заказов → {file_path}")

    def export_client_report(self, file_path: str):
        """Отчёт: клиент + количество и сумма его заказов"""
        query = """
        SELECT 
            c.full_name AS "ФИО",
            COUNT(o.id) AS "Кол-во заказов",
            COALESCE(SUM(o.amount), 0) AS "Общая сумма"
        FROM clients c
        LEFT JOIN orders o ON c.id = o.client_id
        GROUP BY c.id, c.full_name
        ORDER BY "Общая сумма" DESC
        """
        db = DatabaseManager()
        try:
            data = db.execute_query(query)
            df = pd.DataFrame(data, columns=['ФИО', 'Кол-во заказов', 'Общая сумма'])
            df.to_excel(file_path, index=False)
            print(f"Отчёт по клиентам экспортирован → {file_path}")
        finally:
            db.close()

    def close(self):
        self.cm.close()
        self.om.close()
