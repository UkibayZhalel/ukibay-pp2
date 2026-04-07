import psycopg2
from config import load_config


class PhoneBookApp:
    def __init__(self):
        try:
            params = load_config()
            self.conn = psycopg2.connect(**params)
            print("--- Подключено к базе suppliers (Practice 8) ---")
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            exit()

    # --- 1. Поиск по паттерну (Вызов ФУНКЦИИ через SELECT) ---
    def search(self, pattern):
        with self.conn.cursor() as cur:
            # Функции вызываются через SELECT
            cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
            rows = cur.fetchall()
            for row in rows:
                print(f"ID: {row[0]} | Имя: {row[1]} | Тел: {row[2]}")

    # --- 2. Добавить или Обновить (Вызов ПРОЦЕДУРЫ через CALL) ---
    def upsert(self, name, phone):
        with self.conn.cursor() as cur:
            # Процедуры вызываются через CALL
            cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
            self.conn.commit()
            print(f"Контакт {name} обработан (добавлен или обновлен).")

    # --- 3. Удаление (Вызов ПРОЦЕДУРЫ через CALL) ---
    def delete(self, identifier):
        with self.conn.cursor() as cur:
            cur.execute("CALL delete_contact(%s);", (identifier,))
            self.conn.commit()
            print(f"Запись {identifier} удалена.")

    # --- 4. Пагинация (Вызов ФУНКЦИИ через SELECT) ---
    def get_page(self, limit, offset):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
            rows = cur.fetchall()
            print(f"\n--- Страница (лимит {limit}, отступ {offset}) ---")
            for row in rows:
                print(row)

    # --- 5. Массовая вставка с валидацией (Сложная процедура) ---
    def bulk_insert(self, names, phones):
        with self.conn.cursor() as cur:
            try:
                # Передаем списки Python как массивы PostgreSQL
                cur.execute("CALL bulk_insert_with_validation(%s, %s);", (names, phones))
                self.conn.commit()
                # Выводим предупреждения (RAISE NOTICE) из базы, если они были
                for notice in self.conn.notices:
                    print(f"Сообщение от базы: {notice}")
            except Exception as e:
                self.conn.rollback()
                print(f"Ошибка массовой вставки: {e}")

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


# --- МЕНЮ ПРИЛОЖЕНИЯ ---
def main():
    app = PhoneBookApp()

    while True:
        print("1. Поиск по паттерну (Функция)")
        print("2. Добавить/Обновить (Процедура Upsert)")
        print("3. Удалить контакт (Процедура)")
        print("4. Показать страницу (Пагинация)")
        print("5. Массовый тест (Валидация)")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            app.search(input("Введите текст для поиска: "))
        elif choice == '2':
            app.upsert(input("Имя: "), input("Телефон: "))
        elif choice == '3':
            app.delete(input("Имя или телефон для удаления: "))
        elif choice == '4':
            limit = int(input("Сколько записей показать? "))
            offset = int(input("Сколько пропустить? "))
            app.get_page(limit, offset)
        elif choice == '5':
            # Пример: один правильный, один короткий (ошибка)
            names = ["User OK", "User Error"]
            phones = ["+77015554433", "123"]  # "123" не пройдет валидацию length >= 10
            app.bulk_insert(names, phones)
        elif choice == '6':
            break


if __name__ == "__main__":
    main()