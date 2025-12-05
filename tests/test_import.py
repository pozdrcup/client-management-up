# test_import.py
from src.excel_io import ExcelImporter

def main():
    importer = ExcelImporter()
    try:
        importer.import_clients_from_excel("data/clients.xlsx")
        importer.import_orders_from_excel("data/orders.xlsx")
    finally:
        importer.close()

if __name__ == "__main__":
    main()
