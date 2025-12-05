import pandas as pd
from src.client_manager import ClientManager
from src.order_manager import OrderManager
from src.models import Client, Order
import os

class ExcelImporter:
    def __init__(self):
        self.cm = ClientManager()
        self.om = OrderManager()

    def import_clients_from_excel(self, file_path: str):
        """Импортирует клиентов из Excel-файла."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден")

        df = pd.read_excel(file_path)

        required_columns = {'ФИО'}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"В файле должны быть колонки: {required_columns}")

        imported = 0
        for _, row in df.iterrows():
            try:
                client = Client(
                    full_name=row['ФИО'].strip(),
                    contact_info=row.get('Контактная информация', '').strip(),
                    registration_date=row.get('Дата регистрации', None),
                    notes=row.get('Примечания', '').strip()
                )
                self.cm.add_client(client)
                imported += 1
            except Exception as e:
                print(f" Ошибка при импорте клиента '{row.get('ФИО', 'N/A')}': {e}")

        print(f" Импортировано {imported} клиентов из {file_path}")
        return imported

    def import_orders_from_excel(self, file_path: str):
        """Импортирует заказы из Excel-файла."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден")

        df = pd.read_excel(file_path)

        required_columns = {'ID клиента', 'Дата заказа', 'Сумма'}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"В файле должны быть колонки: {required_columns}")

        imported = 0
        for _, row in df.iterrows():
            try:
                client_id = int(row['ID клиента'])
                # Проверим, существует ли клиент
                if not self.cm.get_client_by_id(client_id):
                    print(f" Клиент с ID={client_id} не найден. Заказ пропущен.")
                    continue

                order = Order(
                    client_id=client_id,
                    order_date=row.get('Дата заказа', None),
                    description=row.get('Описание', '').strip(),
                    amount=row.get('Сумма', 0.0)
                )
                self.om.add_order(order)
                imported += 1
            except Exception as e:
                print(f" Ошибка при импорте заказа: {e}")

        print(f" Импортировано {imported} заказов из {file_path}")
        return imported

    def close(self):
        self.cm.close()
        self.om.close()

