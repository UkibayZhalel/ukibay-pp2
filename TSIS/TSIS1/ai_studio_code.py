import json
import csv
import os
from connect import connect
from config import load_config
import psycopg2.extras

class PhoneBookApp:
    def __init__(self):
        self.config = load_config()
        self.conn = connect(self.config)

    def execute_query(self, query, params=None, fetch=False):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params)
            if fetch:
                return cur.fetchall()
            self.conn.commit()

    def call_procedure(self, proc_name, params):
        with self.conn.cursor() as cur:
            cur.execute(f"CALL {proc_name}({','.join(['%s']*len(params))})", params)
            self.conn.commit()

    # --- 3.2 Advanced Search & Filter ---
    def list_contacts(self, filter_group=None, sort_by="name"):
        query = """
            SELECT c.name, c.email, c.birthday, g.name as group_name 
            FROM contacts c LEFT JOIN groups g ON c.group_id = g.id
        """
        params = []
        if filter_group:
            query += " WHERE g.name = %s"
            params.append(filter_group)
        
        allowed_sorts = {"name": "c.name", "birthday": "c.birthday", "date": "c.created_at"}
        query += f" ORDER BY {allowed_sorts.get(sort_by, 'c.name')}"
        
        results = self.execute_query(query, params, fetch=True)
        for row in results:
            print(f"{row['name']} | {row['email']} | {row['birthday']} | Group: {row['group_name']}")

    def paginated_view(self):
        limit = 5
        offset = 0
        while True:
            rows = self.execute_query("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset), fetch=True)
            if not rows and offset > 0:
                print("No more records.")
                offset -= limit
                continue
            
            print(f"\n--- Page {(offset//limit)+1} ---")
            for r in rows:
                print(f"{r['id']}: {r['name']} ({r['email']})")
            
            cmd = input("\n[n]ext, [p]rev, [q]uit: ").lower()
            if cmd == 'n': offset += limit
            elif cmd == 'p': offset = max(0, offset - limit)
            elif cmd == 'q': break

    # --- 3.3 Import / Export ---
    def export_to_json(self, filename="contacts.json"):
        query = """
            SELECT c.*, g.name as group_name, 
            ARRAY(SELECT json_build_object('phone', p.phone, 'type', p.type) FROM phones p WHERE p.contact_id = c.id) as phone_data
            FROM contacts c LEFT JOIN groups g ON c.group_id = g.id
        """
        data = self.execute_query(query, fetch=True)
        # Convert date objects to string for JSON
        for row in data:
            if row['birthday']: row['birthday'] = str(row['birthday'])
            if row['created_at']: row['created_at'] = str(row['created_at'])

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Exported to {filename}")

    def import_from_json(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        
        for item in data:
            # Check for duplicate
            exists = self.execute_query("SELECT id FROM contacts WHERE name = %s", (item['name'],), fetch=True)
            if exists:
                choice = input(f"Contact {item['name']} exists. [S]kip or [O]verwrite? ").lower()
                if choice == 's': continue
                self.execute_query("DELETE FROM contacts WHERE name = %s", (item['name'],))

            # Insert Contact
            self.call_procedure("move_to_group", (item['name'], item.get('group_name', 'Other')))
            self.execute_query(
                "UPDATE contacts SET email=%s, birthday=%s WHERE name=%s",
                (item.get('email'), item.get('birthday'), item['name'])
            )
            # Insert Phones
            for p in item.get('phone_data', []):
                self.call_procedure("add_phone", (item['name'], p['phone'], p['type']))

    def search(self, text):
        results = self.execute_query("SELECT * FROM search_contacts(%s)", (text,), fetch=True)
        for r in results:
            print(f"Name: {r['name']} | Email: {r['email']} | Phones: {r['phone_list']}")

    def menu(self):
        while True:
            print("\n--- Phonebook Extended ---")
            print("1. List & Sort contacts")
            print("2. Search (Advanced)")
            print("3. Paginated View")
            print("4. Add Phone to Contact")
            print("5. Export to JSON")
            print("6. Import from JSON")
            print("0. Exit")
            choice = input("Select: ")

            if choice == '1':
                grp = input("Filter by group (leave empty for all): ")
                srt = input("Sort by (name/birthday/date): ")
                self.list_contacts(grp if grp else None, srt)
            elif choice == '2':
                self.search(input("Enter search query (name/email/phone): "))
            elif choice == '3':
                self.paginated_view()
            elif choice == '4':
                name = input("Contact Name: ")
                ph = input("Phone: ")
                ptype = input("Type (home/work/mobile): ")
                self.call_procedure("add_phone", (name, ph, ptype))
            elif choice == '5':
                self.export_to_json()
            elif choice == '6':
                self.import_from_json("contacts.json")
            elif choice == '0':
                break

if __name__ == "__main__":
    app = PhoneBookApp()
    app.menu()