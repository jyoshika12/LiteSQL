import json
import os

DATA_FILE = "tables.json"

tables = {}

def save_to_disk():
    with open(DATA_FILE, "w") as f:
        json.dump(tables, f)

def load_from_disk():
    global tables
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            tables = json.load(f)

def create_table(name, columns, primary_key=None):
    if name in tables:
        raise Exception("Table already exists")

    tables[name] = {
        "columns": columns,
        "rows": [],
        "indexes": {}
    }

    if primary_key:
        tables[name]["indexes"][primary_key] = {}

    save_to_disk()

def insert_into(name, values):
    if name not in tables:
        raise Exception("Table doesn't exist")
    if len(values) != len(tables[name]["columns"]):
        raise Exception("Column count doesn't match")

    tables[name]["rows"].append(values)

    for col in tables[name]["indexes"]:
        col_idx = tables[name]["columns"].index(col)
        key = values[col_idx]
        tables[name]["indexes"][col].setdefault(key, []).append(values)

    save_to_disk()

def delete_from(name, where):
    if name not in tables:
        raise Exception("Table doesn't exist")

    col_names = tables[name]["columns"]
    indexes = tables[name]["indexes"]
    new_rows = []
    deleted = 0

    for row in tables[name]["rows"]:
        if where(row, col_names):
            
            for col in indexes:
                col_idx = col_names.index(col)
                key = row[col_idx]
                if key in indexes[col]:
                    indexes[col][key].remove(row)
                    if not indexes[col][key]:
                        del indexes[col][key]
            deleted += 1
        else:
            new_rows.append(row)

    tables[name]["rows"] = new_rows
    save_to_disk()
    return deleted

def update_table(name, column, value, where):
    if name not in tables:
        raise Exception("Table doesn't exist")

    count = 0
    col_names = tables[name]["columns"]
    col_idx = col_names.index(column)
    indexes = tables[name]["indexes"]

    for row in tables[name]["rows"]:
        if where(row, col_names):
            for col in indexes:
                if column == col:
                    old_key = row[col_idx]
                    if old_key in indexes[col]:
                        indexes[col][old_key].remove(row)
                        if not indexes[col][old_key]:
                            del indexes[col][old_key]
            row[col_idx] = value
            count += 1
            for col in indexes:
                col_idx2 = col_names.index(col)
                key = row[col_idx2]
                indexes[col].setdefault(key, []).append(row)

    save_to_disk()
    return count

def select_all(name, where=None):
    if name not in tables:
        raise Exception("Table doesn't exist")

    col_names = tables[name]["columns"]
    results = []

    if where and "indexes" in tables[name]:
        try:
            code = where.__code__
            col_name = code.co_consts[1]
            val = code.co_consts[2]
            if col_name in tables[name]["indexes"]:
                return col_names, tables[name]["indexes"][col_name].get(val, [])
        except:
            pass

    for row in tables[name]["rows"]:
        if where is None or where(row, col_names):
            results.append(row)

    return col_names, results

def drop_table(name):
    if name not in tables:
        raise Exception("Table doesn't exist")
    del tables[name]
    save_to_disk()

def list_tables():
    return list(tables.keys())

def describe_table(name):
    if name not in tables:
        raise Exception("Table doesn't exist")
    return tables[name]["columns"]
