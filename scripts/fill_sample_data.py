import pandas as pd
from pathlib import Path

# Создаём папку data, если её нет
Path("data").mkdir(exist_ok=True)

# Заполняем clients.xlsx
pd.DataFrame([{
    "ФИО": "Иванов Иван Иванович",
    "Контактная информация": "ivanov@example.com",
    "Дата регистрации": "2025-12-05",
    "Примечания": "Тестовый клиент для проверки импорта"
}]).to_excel("data/clients.xlsx", index=False)

# Заполняем orders.xlsx
pd.DataFrame([{
    "ID клиента": 1,
    "Дата заказа": "2025-12-05",
    "Описание": "Первичная консультация",
    "Сумма": 1500.00
}]).to_excel("data/orders.xlsx", index=False)

print("✅ Файлы data/clients.xlsx и data/orders.xlsx заполнены тестовыми данными.")
