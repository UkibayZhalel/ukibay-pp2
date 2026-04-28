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
            cur.execute(f"CALL {proc_name}({','.join(['%s'] * len(params))})", params)
            self.conn.commit()

    # --- CRUD OPERATIONS ---

    def create_contact(self):
        print("\n--- Create New Contact ---")
        name = input("Name: ")
        email = input("Email: ")
        birthday = input("Birthday (YYYY-MM-DD) or leave empty: ") or None
        group = input("Group (Family, Work, etc.): ")
        phone = input("Phone Number: ")
        ptype = input("Phone Type (home/work/mobile): ")

        # 1. Create contact and group
        self.call_procedure("move_to_group", (name, group))
        # 2. Update email and birthday
        self.execute_query("UPDATE contacts SET email=%s, birthday=%s WHERE name=%s", (email, birthday, name))
        # 3. Add phone
        self.call_procedure("add_phone", (name, phone, ptype))
        print("Contact created successfully!")

    def update_contact(self):
        name = input("\nEnter the Name of the contact to update: ")
        # Check if exists
        contact = self.execute_query("SELECT * FROM contacts WHERE name=%s", (name,), fetch=True)
        if not contact:
            print("Contact not found.")
            return

        print("Leave field empty to keep current value.")
        new_email = input(f"New Email [{contact[0]['email']}]: ") or contact[0]['email']
        new_bday = input(f"New Birthday [{contact[0]['birthday']}]: ") or contact[0]['birthday']
        new_group = input(f"New Group: ")

        if new_group:
            self.call_procedure("move_to_group", (name, new_group))

        self.execute_query("UPDATE contacts SET email=%s, birthday=%s WHERE name=%s", (new_email, new_bday, name))
        print("Contact updated.")

    def delete_contact(self):
        name = input("\nEnter Name to DELETE: ")
        confirm = input(f"Are you sure you want to delete {name}? (y/n): ")
        if confirm.lower() == 'y':
            self.call_procedure("delete_contact", (name,))
            print("Contact deleted.")

    # --- DATA EXCHANGE ---

    def import_from_json(self, filename="contacts.json"):
        if not os.path.exists(filename):
            print("File not found.")
            return

        with open(filename, 'r') as f:
            data = json.load(f)

        for item in data:
            name = item['name']
            # Check for duplicate
            exists = self.execute_query("SELECT id FROM contacts WHERE name = %s", (name,), fetch=True)

            if exists:
                choice = input(f"\nContact '{name}' already exists. [S]kip or [O]verwrite? ").lower()
                if choice == 's':
                    continue
                else:
                    self.call_procedure("delete_contact", (name,))

            # Insert logic
            self.call_procedure("move_to_group", (name, item.get('group_name', 'Other')))
            self.execute_query(
                "UPDATE contacts SET email=%s, birthday=%s WHERE name=%s",
                (item.get('email'), item.get('birthday'), name)
            )
            # Add phones if they exist in JSON
            if 'phone_data' in item and item['phone_data']:
                for p in item['phone_data']:
                    self.call_procedure("add_phone", (name, p['phone'], p['type']))

        print("\nJSON Import completed.")

    def export_to_json(self, filename="contacts.json"):
        query = """
            SELECT c.name, c.email, c.birthday, g.name as group_name,
            (SELECT json_agg(json_build_object('phone', p.phone, 'type', p.type)) 
             FROM phones p WHERE p.contact_id = c.id) as phone_data
            FROM contacts c LEFT JOIN groups g ON c.group_id = g.id
        """
        data = self.execute_query(query, fetch=True)
        for row in data:
            if row['birthday']: row['birthday'] = str(row['birthday'])

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Exported to {filename}")

    # --- DISPLAY ---

    def search(self):
        q = input("Search by name, email, or phone: ")
        results = self.execute_query("SELECT * FROM search_contacts(%s)", (q,), fetch=True)
        if not results:
            print("No matches found.")
            return
        for r in results:
            print(f"[{r['group_name']}] {r['name']} - {r['email']} | Phones: {r['phone_list']}")

    def menu(self):
        while True:
            print("\n--- PhoneBook TSIS 1 ---")
            print("1. Add New Contact")
            print("2. Search / List Contacts")
            print("3. Update Contact")
            print("4. Delete Contact")
            print("5. Import from CSV")
            print("6. Import from JSON")
            print("7. Export to JSON")
            print("0. Exit")

            choice = input("\nSelect an option: ")

            if choice == '1':
                self.create_contact()
            elif choice == '2':
                self.search()
            elif choice == '3':
                self.update_contact()
            elif choice == '4':
                self.delete_contact()
            elif choice == '5':
                print("CSV Import triggered...");  # add your CSV import call here
            elif choice == '6':
                self.import_from_json()
            elif choice == '7':
                self.export_to_json()
            elif choice == '0':
                break
            else:
                print("Invalid choice.")


if __name__ == "__main__":
    app = PhoneBookApp()
    app.menu()