# test_order_module.py — запустите: python test_order_module.py

from src.client_manager import ClientManager
from src.order_manager import OrderManager
from src.models import Client, Order

def test_order_module():
    cm = ClientManager()
    om = OrderManager()

    print("Добавляем клиента...")
    client = Client("Сидоров С.С.", "sidorov@example.com", "2025-12-01", "Новый клиент")
    cm.add_client(client)

    clients = cm.get_all_clients()
    client_id = clients[0][0]  # берем ID первого клиента
    print(f"Клиент добавлен с ID = {client_id}")

    print("Добавляем заказ...")
    order = Order(
        client_id=client_id,
        order_date="2025-12-05",
        description="Покупка товара A",
        amount=2500.50
    )
    om.add_order(order)

    print("Получаем все заказы...")
    all_orders = om.get_all_orders()
    print("Все заказы:", all_orders)

    print("Получаем заказы клиента...")
    client_orders = om.get_orders_by_client(client_id)
    print(f"Заказы клиента {client_id}:", client_orders)

    print("Поиск заказа по 'товар'...")
    found = om.search_orders("товар")
    print("Результаты поиска:", found)

    print("✅ Все операции с заказами выполнены успешно!")

    cm.close()
    om.close()

if __name__ == "__main__":
    test_order_module()
