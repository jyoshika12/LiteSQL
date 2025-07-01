from parser import parse_command
from storage import (
    create_table, insert_into, select_all, delete_from, update_table,
    drop_table, list_tables, describe_table, load_from_disk
)

from tabulate import tabulate

print("Welcome to MiniRDBMS. Type your SQL commands:")
load_from_disk()

while True:
    try:
        command = input("mydb> ")
        parsed = parse_command(command)

        if parsed[0] == "CREATE":
            _, name, cols, pk = parsed
            create_table(name, cols, pk)
            if pk:
                print(f"Table '{name}' created with PRIMARY KEY on '{pk}'.")
            else:
                print(f"Table '{name}' created.")

        elif parsed[0] == "INSERT":
            _, name, values = parsed
            insert_into(name, values)
            print("1 row inserted.")

        elif parsed[0] == "SELECT":
            _, name, where = parsed
            cols, rows = select_all(name, where)
            print(tabulate(rows, headers=cols, tablefmt="grid"))

        elif parsed[0] == "DELETE":
            _, name, where = parsed
            deleted = delete_from(name, where)
            print(f"{deleted} row(s) deleted.")

        elif parsed[0] == "UPDATE":
            _, name, col, val, where = parsed
            updated = update_table(name, col, val, where)
            print(f"{updated} row(s) updated.")

        elif parsed[0] == "DROP":
            _, name = parsed
            drop_table(name)
            print(f"Table '{name}' dropped.")

        elif parsed[0] == "SHOW_TABLES":
            tables = list_tables()
            if tables:
                print("Tables:")
                for t in tables:
                    print("-", t)
            else:
                print("No tables found.")

        elif parsed[0] == "DESCRIBE":
            _, name = parsed
            cols = describe_table(name)
            print(f"Table '{name}' columns: {', '.join(cols)}")

        else:
            print("Unknown command.")

    except Exception as e:
        print("Error:", e)
