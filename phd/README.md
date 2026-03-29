# LedgerLite

LedgerLite is a simple and professional accounting mini-project built for the course requirement described in the provided PDF. It focuses on one clear vertical slice: entering, storing, reviewing, exporting, and restoring accounting transactions.

## Project Idea

This application solves a small but realistic accounting problem: tracking daily income and expense entries for a small business or office. It allows the user to:

- create accounting entries
- update and delete entries
- store data in a relational database
- export data to `CSV`, `JSON`, and `TXT`
- import a backup from `CSV` or `JSON`
- view a live dashboard with totals and balance

## Stack

- Python
- Flask
- SQLite
- HTML / CSS

## Run

1. Install Python 3.11 or later.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the application:

```bash
python app.py
```

4. Open `http://127.0.0.1:5000`

## Assignment Mapping

- Part 1, Python Basics:
  variables, conditions, loops, validation, modular functions
- Part 2, Files and Data Handling:
  CSV / JSON import-export and TXT reporting
- Part 3, Database Management:
  SQLite persistence with CRUD operations
- Part 4(1), Web Interface:
  Flask dashboard and forms
- Part 4(2), OOP:
  `Transaction`, `TransactionRepository`, and `AccountingService`
- Part 5, Engineering Standards:
  structured project layout, validation, error messaging, and Git-ready files

## Suggested Accounting Use Case

The project is suitable for:

- a small accounting office
- a local store
- a student finance simulation
- a simple bookkeeping demo
