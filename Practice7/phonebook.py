import psycopg2
from psycopg2 import extras
import csv
import os
from config import load_config


class PhoneBook:
    def __init__(self):
        try:
            # Загружаем твои данные из suppliers
            params = load_config()
            self.conn = psycopg2.connect(**params)
            self.create_table()
            print("--- Успешное подключение к базе 'suppliers' ---")
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            os._exit(1)

    def create_table(self):
        """Создание таблицы контактов"""
        query = """
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) UNIQUE NOT NULL
        );
        """
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()

    def insert_contact(self, name, phone):
        """1. Вставка данных из консоли"""
        query = "INSERT INTO contacts (name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING"
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, (name, phone))
                self.conn.commit()
                print(f"Контакт '{name}' сохранен.")
        except Exception as e:
            self.conn.rollback()
            print(f"Ошибка вставки: {e}")

    def insert_from_csv(self, file_path):
        """Импорт из CSV с объединением Имени и Фамилии"""
        if not os.path.exists(file_path):
            print(f"Файл {file_path} не найден!")
            return

        query = "INSERT INTO contacts (name, phone) VALUES %s ON CONFLICT (phone) DO NOTHING"

        try:
            contacts_to_insert = []
            with open(file_path, 'r', encoding='utf-8') as f:
                # Используем DictReader, чтобы обращаться к колонкам по именам
                reader = csv.DictReader(f)
                for row in reader:
                    # Объединяем Имя и Фамилию в одну строку для колонки 'name'
                    full_name = f"{row['first_name']} {row['last_name']}"
                    phone = row['phone']
                    contacts_to_insert.append((full_name, phone))

            with self.conn.cursor() as cur:
                # Массовая вставка подготовленного списка кортежей
                extras.execute_values(cur, query, contacts_to_insert)
                self.conn.commit()
                print(f"--- Успешно импортировано {len(contacts_to_insert)} контактов из CSV ---")

        except Exception as e:
            self.conn.rollback()
            print(f"Ошибка при чтении CSV: {e}")


    def update_contact(self, name, new_phone):
        """3. Обновление номера по имени"""
        query = "UPDATE contacts SET phone = %s WHERE name = %s"
        with self.conn.cursor() as cur:
            cur.execute(query, (new_phone, name))
            self.conn.commit()
            print("Данные обновлены (если контакт существовал).")

    def query_contacts(self, search):
        """4. Поиск с фильтрами"""
        # Поиск по имени (регистронезависимо) или по началу номера
        query = "SELECT * FROM contacts WHERE name ILIKE %s OR phone LIKE %s"
        with self.conn.cursor() as cur:
            cur.execute(query, (f"%{search}%", f"{search}%"))
            rows = cur.fetchall()
            if not rows:
                print("Ничего не найдено.")
            for row in rows:
                print(f"ID: {row[0]} | Имя: {row[1]} | Тел: {row[2]}")

    def delete_contact(self, identifier):
        """5. Удаление по имени или телефону"""
        query = "DELETE FROM contacts WHERE name = %s OR phone = %s"
        with self.conn.cursor() as cur:
            cur.execute(query, (identifier, identifier))
            self.conn.commit()
            print(f"Контакт '{identifier}' удален.")

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


def main():
    app = PhoneBook()

    while True:
        print("\n--- PhoneBook (Database: suppliers) ---")
        print("1. Добавить контакт (Консоль)")
        print("2. Импорт из CSV")
        print("3. Поиск (по имени или префиксу телефона)")
        print("4. Обновить телефон")
        print("5. Удалить контакт")
        print("6. Выход")

        choice = input("\nВыберите номер действия: ")

        if choice == '1':
            app.insert_contact(input("Имя: "), input("Телефон: "))
        elif choice == '2':
            app.insert_from_csv(input("Введите имя CSV файла (например, data.csv): "))
        elif choice == '3':
            app.query_contacts(input("Введите имя или начало номера: "))
        elif choice == '4':
            app.update_contact(input("Введите имя: "), input("Введите новый телефон: "))
        elif choice == '5':
            app.delete_contact(input("Введите имя или номер для удаления: "))
        elif choice == '6':
            print("Пока!")
            break


if __name__ == "__main__":
    main()