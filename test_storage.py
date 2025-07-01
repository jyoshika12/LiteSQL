import pytest
from storage import create_table, insert_into, select_all, delete_from, update_table, drop_table, tables

def setup_function():
    # Reset global state before each test
    tables.clear()

def test_create_and_insert():
    create_table("students", ["id", "name", "marks"], primary_key="id")
    insert_into("students", [1, "Jyoshika", 92])
    insert_into("students", [2, "Ravi", 85])

    assert "students" in tables
    assert len(tables["students"]["rows"]) == 2

def test_select_with_primary_key_index():
    create_table("books", ["book_id", "title"], primary_key="book_id")
    insert_into("books", [101, "Clean Code"])
    insert_into("books", [102, "DBMS Bible"])
    _, result = select_all("books", where=lambda row, cols: row[cols.index("book_id")] == 102)

    assert len(result) == 1
    assert result[0][1] == "DBMS Bible"

def test_delete():
    create_table("users", ["id", "name"], primary_key="id")
    insert_into("users", [1, "A"])
    insert_into("users", [2, "B"])
    deleted = delete_from("users", where=lambda row, cols: row[cols.index("id")] == 1)

    assert deleted == 1
    assert len(tables["users"]["rows"]) == 1

def test_update():
    create_table("courses", ["code", "title"], primary_key="code")
    insert_into("courses", ["CS101", "Intro"])
    update_table("courses", "title", "Intro to CS", where=lambda row, cols: row[cols.index("code")] == "CS101")

    _, rows = select_all("courses")
    assert rows[0][1] == "Intro to CS"
