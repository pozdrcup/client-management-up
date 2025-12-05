# Цель  
Разработать модуль для ввода, хранения, поиска и отчётности по клиентам малого бизнеса.

# Технологии
- Python 3.10+
- PostgreSQL
- Tkinter (GUI)
- pandas + openpyxl (Excel)
- Git

# Установка
1. `git clone <ваш_репозиторий>`
2. `cd client-management-system`
3. `python -m venv venv && source venv/bin/activate` *(Linux/Mac)*  
   или `venv\Scripts\activate` *(Windows)*
4. `pip install -r requirements.txt`
5. Создайте БД и таблицы:  
   ```bash
   psql -U postgres -f scripts/init_db.sql
