import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from src.client_manager import ClientManager
from src.order_manager import OrderManager
from src.excel_io import ExcelExporter

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Учет клиентов")
        self.root.geometry("800x600")

        # Инициализация менеджеров
        self.cm = ClientManager()
        self.om = OrderManager()
        self.exporter = ExcelExporter()

        # Создание вкладок
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Вкладка "Клиенты"
        self.clients_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.clients_frame, text="Клиенты")

        # Вкладка "Заказы"
        self.orders_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.orders_frame, text="Заказы")

        # Вкладка "Отчеты"
        self.reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reports_frame, text="Отчеты")

        # Инициализация интерфейса
        self.init_clients_ui()
        self.init_orders_ui()
        self.init_reports_ui()

    def init_clients_ui(self):
        """Инициализация интерфейса вкладки "Клиенты"."""
        # Кнопки управления
        btn_frame = ttk.Frame(self.clients_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)

        add_btn = ttk.Button(btn_frame, text="Добавить клиента", command=self.add_client)
        add_btn.pack(side='left', padx=5)

        edit_btn = ttk.Button(btn_frame, text="Редактировать", command=self.edit_client)
        edit_btn.pack(side='left', padx=5)

        delete_btn = ttk.Button(btn_frame, text="Удалить", command=self.delete_client)
        delete_btn.pack(side='left', padx=5)

        search_btn = ttk.Button(btn_frame, text="Поиск", command=self.search_clients)
        search_btn.pack(side='left', padx=5)

        refresh_btn = ttk.Button(btn_frame, text="Обновить", command=self.load_clients)
        refresh_btn.pack(side='left', padx=5)

        # Таблица клиентов
        tree_frame = ttk.Frame(self.clients_frame)
        tree_frame.pack(fill='both', expand=True, padx=5, pady=5)

        columns = ('ID', 'ФИО', 'Контактная информация', 'Дата регистрации', 'Примечания')
        self.clients_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        for col in columns:
            self.clients_tree.heading(col, text=col)
            self.clients_tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.clients_tree.yview)
        self.clients_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.clients_tree.pack(fill='both', expand=True)

        # Загрузка данных при запуске
        self.load_clients()

        # Обработчик двойного клика для редактирования
        self.clients_tree.bind('<Double-1>', lambda event: self.edit_client())

    def load_clients(self):
        """Загрузка всех клиентов из БД в таблицу."""
        for item in self.clients_tree.get_children():
            self.clients_tree.delete(item)

        clients = self.cm.get_all_clients()
        for client in clients:
            self.clients_tree.insert('', tk.END, values=client)

    def add_client(self):
        """Открытие диалогового окна для добавления нового клиента."""
        AddClientDialog(self.root, self.cm, self.load_clients)

    def edit_client(self):
        """Редактирование выбранного клиента."""
        selected_item = self.clients_tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Выберите клиента для редактирования!")
            return

        item_values = self.clients_tree.item(selected_item[0], 'values')
        client_id = int(item_values[0])

        EditClientDialog(self.root, self.cm, client_id, self.load_clients)

    def delete_client(self):
        """Удаление выбранного клиента."""
        selected_item = self.clients_tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Выберите клиента для удаления!")
            return

        item_values = self.clients_tree.item(selected_item[0], 'values')
        client_id = int(item_values[0])
        full_name = item_values[1]

        confirm = messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить клиента {full_name}?")
        if confirm:
            self.cm.delete_client(client_id)
            self.load_clients()

    def search_clients(self):
        """Поиск клиентов по введенному запросу."""
        search_term = simpledialog.askstring("Поиск", "Введите запрос:")
        if not search_term:
            return

        for item in self.clients_tree.get_children():
            self.clients_tree.delete(item)

        clients = self.cm.search_clients(search_term)
        for client in clients:
            self.clients_tree.insert('', tk.END, values=client)

    def init_orders_ui(self):
        """Инициализация интерфейса вкладки "Заказы"."""
        # Кнопки управления
        btn_frame = ttk.Frame(self.orders_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)

        add_btn = ttk.Button(btn_frame, text="Добавить заказ", command=self.add_order)
        add_btn.pack(side='left', padx=5)

        refresh_btn = ttk.Button(btn_frame, text="Обновить", command=self.load_orders)
        refresh_btn.pack(side='left', padx=5)

        # Таблица заказов
        tree_frame = ttk.Frame(self.orders_frame)
        tree_frame.pack(fill='both', expand=True, padx=5, pady=5)

        columns = ('ID', 'ID клиента', 'Дата заказа', 'Описание', 'Сумма')
        self.orders_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        for col in columns:
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.orders_tree.pack(fill='both', expand=True)

        self.load_orders()

    def load_orders(self):
        """Загрузка всех заказов из БД в таблицу."""
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        orders = self.om.get_all_orders()
        for order in orders:
            self.orders_tree.insert('', tk.END, values=order)

    def add_order(self):
        """Открытие диалогового окна для добавления нового заказа."""
        AddOrderDialog(self.root, self.cm, self.om, self.load_orders)

    def init_reports_ui(self):
        """Инициализация интерфейса вкладки "Отчеты"."""
        # Кнопки экспорта
        btn_frame = ttk.Frame(self.reports_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)

        export_clients_btn = ttk.Button(btn_frame, text="Экспорт клиентов в Excel", command=self.export_clients)
        export_clients_btn.pack(side='left', padx=5)

        export_orders_btn = ttk.Button(btn_frame, text="Экспорт заказов в Excel", command=self.export_orders)
        export_orders_btn.pack(side='left', padx=5)

    def export_clients(self):
        """Экспорт клиентов в Excel."""
        try:
            self.exporter.export_clients_to_excel("export/clients_export.xlsx")
            messagebox.showinfo("Успех", "Клиенты успешно экспортированы в Excel!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {e}")

    def export_orders(self):
        """Экспорт заказов в Excel."""
        try:
            self.exporter.export_orders_to_excel("export/orders_export.xlsx")
            messagebox.showinfo("Успех", "Заказы успешно экспортированы в Excel!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {e}")

    def close(self):
        """Закрытие соединений с БД."""
        self.cm.close()
        self.om.close()
        self.exporter.close()


class AddClientDialog:
    """Диалоговое окно для добавления клиента."""
    def __init__(self, parent, client_manager, on_save_callback):
        self.parent = parent
        self.cm = client_manager
        self.on_save_callback = on_save_callback

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Добавить клиента")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)  # Делаем модальным
        self.dialog.grab_set()  # Блокируем родительское окно

        # Поля ввода
        tk.Label(self.dialog, text="ФИО:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.full_name_entry = tk.Entry(self.dialog, width=40)
        self.full_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.dialog, text="Контактная информация:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.contact_info_entry = tk.Entry(self.dialog, width=40)
        self.contact_info_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.dialog, text="Дата регистрации (ГГГГ-ММ-ДД):").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.reg_date_entry = tk.Entry(self.dialog, width=40)
        self.reg_date_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.dialog, text="Примечания:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.notes_entry = tk.Text(self.dialog, width=37, height=5)
        self.notes_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопки
        save_btn = ttk.Button(self.dialog, text="Сохранить", command=self.save_client)
        save_btn.grid(row=4, column=0, columnspan=2, pady=10)

        cancel_btn = ttk.Button(self.dialog, text="Отмена", command=self.dialog.destroy)
        cancel_btn.grid(row=5, column=0, columnspan=2, pady=5)

    def save_client(self):
        """Сохранение клиента в БД."""
        full_name = self.full_name_entry.get().strip()
        contact_info = self.contact_info_entry.get().strip()
        reg_date = self.reg_date_entry.get().strip()
        notes = self.notes_entry.get("1.0", tk.END).strip()

        if not full_name:
            messagebox.showerror("Ошибка", "ФИО обязательно!")
            return

        try:
            # Создаем объект клиента
            from src.models import Client
            client = Client(full_name, contact_info, reg_date, notes)
            self.cm.add_client(client)
            messagebox.showinfo("Успех", "Клиент успешно добавлен!")
            self.dialog.destroy()
            self.on_save_callback()  # Обновляем таблицу
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить клиента: {e}")


class EditClientDialog:
    """Диалоговое окно для редактирования клиента."""
    def __init__(self, parent, client_manager, client_id, on_save_callback):
        self.parent = parent
        self.cm = client_manager
        self.client_id = client_id
        self.on_save_callback = on_save_callback

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Редактировать клиента")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Получаем данные клиента
        clients = self.cm.get_all_clients()
        client_data = None
        for c in clients:
            if c[0] == client_id:  # ID клиента
                client_data = c
                break

        if not client_data:
            messagebox.showerror("Ошибка", "Клиент не найден!")
            self.dialog.destroy()
            return

        # Поля ввода
        tk.Label(self.dialog, text="ФИО:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.full_name_entry = tk.Entry(self.dialog, width=40)
        self.full_name_entry.insert(0, client_data[1])  # ФИО
        self.full_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.dialog, text="Контактная информация:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.contact_info_entry = tk.Entry(self.dialog, width=40)
        self.contact_info_entry.insert(0, client_data[2] or "")  # Контактная информация
        self.contact_info_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.dialog, text="Дата регистрации (ГГГГ-ММ-ДД):").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.reg_date_entry = tk.Entry(self.dialog, width=40)
        self.reg_date_entry.insert(0, str(client_data[3]))  # Дата регистрации
        self.reg_date_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.dialog, text="Примечания:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.notes_entry = tk.Text(self.dialog, width=37, height=5)
        self.notes_entry.insert("1.0", client_data[4] or "")  # Примечания
        self.notes_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопки
        save_btn = ttk.Button(self.dialog, text="Сохранить", command=self.save_client)
        save_btn.grid(row=4, column=0, columnspan=2, pady=10)

        cancel_btn = ttk.Button(self.dialog, text="Отмена", command=self.dialog.destroy)
        cancel_btn.grid(row=5, column=0, columnspan=2, pady=5)

    def save_client(self):
        """Сохранение изменений клиента в БД."""
        full_name = self.full_name_entry.get().strip()
        contact_info = self.contact_info_entry.get().strip()
        reg_date = self.reg_date_entry.get().strip()
        notes = self.notes_entry.get("1.0", tk.END).strip()

        if not full_name:
            messagebox.showerror("Ошибка", "ФИО обязательно!")
            return

        try:
            # Создаем объект клиента
            from src.models import Client
            client = Client(full_name, contact_info, reg_date, notes)
            self.cm.update_client(self.client_id, client)
            messagebox.showinfo("Успех", "Клиент успешно обновлен!")
            self.dialog.destroy()
            self.on_save_callback()  # Обновляем таблицу
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить клиента: {e}")


class AddOrderDialog:
    """Диалоговое окно для добавления заказа."""
    def __init__(self, parent, client_manager, order_manager, on_save_callback):
        self.parent = parent
        self.cm = client_manager
        self.om = order_manager
        self.on_save_callback = on_save_callback

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Добавить заказ")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Получаем список клиентов для выбора
        clients = self.cm.get_all_clients()
        self.client_ids = [c[0] for c in clients]
        self.client_names = [c[1] for c in clients]

        tk.Label(self.dialog, text="Клиент:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.client_var = tk.StringVar()
        self.client_combobox = ttk.Combobox(self.dialog, textvariable=self.client_var, values=self.client_names, state='readonly')
        self.client_combobox.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.dialog, text="Дата заказа (ГГГГ-ММ-ДД):").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.order_date_entry = tk.Entry(self.dialog, width=40)
        self.order_date_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.dialog, text="Описание:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.description_entry = tk.Entry(self.dialog, width=40)
        self.description_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.dialog, text="Сумма:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.amount_entry = tk.Entry(self.dialog, width=40)
        self.amount_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопки
        save_btn = ttk.Button(self.dialog, text="Сохранить", command=self.save_order)
        save_btn.grid(row=4, column=0, columnspan=2, pady=10)

        cancel_btn = ttk.Button(self.dialog, text="Отмена", command=self.dialog.destroy)
        cancel_btn.grid(row=5, column=0, columnspan=2, pady=5)

    def save_order(self):
        """Сохранение заказа в БД."""
        selected_client_name = self.client_var.get()
        if not selected_client_name:
            messagebox.showerror("Ошибка", "Выберите клиента!")
            return

        # Находим ID клиента
        client_id = None
        clients = self.cm.get_all_clients()
        for c in clients:
            if c[1] == selected_client_name:
                client_id = c[0]
                break

        order_date = self.order_date_entry.get().strip()
        description = self.description_entry.get().strip()
        amount_str = self.amount_entry.get().strip()

        if not order_date or not amount_str:
            messagebox.showerror("Ошибка", "Дата заказа и сумма обязательны!")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма должна быть числом!")
            return

        try:
            # Создаем объект заказа
            from src.models import Order
            order = Order(client_id, order_date, description, amount)
            self.om.add_order(order)
            messagebox.showinfo("Успех", "Заказ успешно добавлен!")
            self.dialog.destroy()
            self.on_save_callback()  # Обновляем таблицу
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить заказ: {e}")


def main():
    root = tk.Tk()
    app = ClientApp(root)

    # Закрытие соединений при закрытии окна
    root.protocol("WM_DELETE_WINDOW", app.close)

    root.mainloop()


if __name__ == "__main__":
    main()
