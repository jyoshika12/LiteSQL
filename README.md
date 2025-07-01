# LiteSQL

A lightweight custom-built SQL engine written in Python — simulating a mini relational database management system (Mini RDBMS) with in-memory tables, indexing, and persistent storage.
It supports core SQL commands, persistent storage, in-memory indexing, and command-line interaction — inspired by how real DBMS systems like SQLite work under the hood.

---

## 🚀 Features

- 🗃️ `CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`, `DROP`
- 🔑 `PRIMARY KEY` support with **automatic indexing**
- 📄 Persistent storage using JSON file (`tables.json`)
- ⚡ Fast lookup using hash-based index
- 🧾 SQL-like syntax (e.g. `SELECT * FROM users WHERE id == 1`)
- 💻 Simple CLI shell (REPL) to interact with the database
- ✅ Unit-tested using `pytest`
- 🧠 Designed with core **DBMS fundamentals** in mind

---

## 🧠 Technologies Used

- Python 3.10
- `json` for persistence
- `tabulate` for pretty CLI tables
- `pytest` for automated testing

---

## 📂 Project Structure
LiteSQL/
│
├── main.py # Command-line interface (REPL)
├── parser.py # SQL parser for commands
├── storage.py # Table creation, query logic, and index management
├── test_storage.py # Unit tests using pytest
├── tables.json # Auto-generated persistent data file
├── .gitignore # Ignore cache and build files
└── README.md # You're here



---

## ▶️ How to Run

### 1. Install dependencies
```bash
pip install tabulate pytest
python main.py



## Sample Commands
-- Create a table with a PRIMARY KEY (auto-indexed)
CREATE TABLE students (id PRIMARY KEY, name, marks);

-- Insert rows
INSERT INTO students VALUES (1, 'Jyoshika', 92);
INSERT INTO students VALUES (2, 'Aarav', 88);

-- Query using indexed column
SELECT * FROM students WHERE id == 2;

-- Update a row
UPDATE students SET marks = 90 WHERE id == 2;

-- Delete a row
DELETE FROM students WHERE id == 1;

-- Describe table structure
DESCRIBE students;

-- View all tables
SHOW TABLES;


##Run Tests
pytest

