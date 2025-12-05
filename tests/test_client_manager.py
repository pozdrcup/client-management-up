from src.client_manager import ClientManager
from src.models import Client

cm = ClientManager()

# Добавляем клиента
new_client = Client("Иванов Иван Иванович", "ivanov@example.com", "2023-12-05", "Хороший клиент")
cm.add_client(new_client)

# Получаем всех клиентов
clients = cm.get_all_clients()
print(clients)

# Поиск
found = cm.search_clients("Иванов")
print(found)

cm.close()
