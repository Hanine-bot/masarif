from __future__ import annotations

import sqlite3
from pathlib import Path

from .models import Transaction


class TransactionRepository:
    def __init__(self, database_path: Path) -> None:
        self.database_path = Path(database_path)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def init_schema(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_date TEXT NOT NULL,
                    entry_type TEXT NOT NULL CHECK (entry_type IN ('income', 'expense')),
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL,
                    payment_method TEXT NOT NULL,
                    reference TEXT DEFAULT '',
                    notes TEXT DEFAULT '',
                    created_at TEXT NOT NULL
                )
                """
            )

    def list_transactions(self, search: str = "", entry_type: str = "") -> list[dict]:
        clauses: list[str] = []
        params: list[object] = []

        if search:
            clauses.append("(description LIKE ? OR category LIKE ? OR reference LIKE ?)")
            needle = f"%{search.strip()}%"
            params.extend([needle, needle, needle])

        if entry_type in {"income", "expense"}:
            clauses.append("entry_type = ?")
            params.append(entry_type)

        where_clause = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        query = f"""
            SELECT *
            FROM transactions
            {where_clause}
            ORDER BY transaction_date DESC, id DESC
        """
        with self._connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]

    def get_transaction(self, transaction_id: int) -> dict | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM transactions WHERE id = ?",
                (transaction_id,),
            ).fetchone()
        return dict(row) if row else None

    def create_transaction(self, transaction: Transaction) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO transactions (
                    transaction_date,
                    entry_type,
                    category,
                    description,
                    amount,
                    payment_method,
                    reference,
                    notes,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    transaction.transaction_date,
                    transaction.entry_type,
                    transaction.category,
                    transaction.description,
                    round(float(transaction.amount), 2),
                    transaction.payment_method,
                    transaction.reference,
                    transaction.notes,
                    transaction.created_at,
                ),
            )
            return int(cursor.lastrowid)

    def update_transaction(self, transaction_id: int, transaction: Transaction) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE transactions
                SET transaction_date = ?,
                    entry_type = ?,
                    category = ?,
                    description = ?,
                    amount = ?,
                    payment_method = ?,
                    reference = ?,
                    notes = ?
                WHERE id = ?
                """,
                (
                    transaction.transaction_date,
                    transaction.entry_type,
                    transaction.category,
                    transaction.description,
                    round(float(transaction.amount), 2),
                    transaction.payment_method,
                    transaction.reference,
                    transaction.notes,
                    transaction_id,
                ),
            )

    def delete_transaction(self, transaction_id: int) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))

    def transaction_summary(self) -> dict[str, float | int]:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    COALESCE(SUM(CASE WHEN entry_type = 'income' THEN amount END), 0) AS total_income,
                    COALESCE(SUM(CASE WHEN entry_type = 'expense' THEN amount END), 0) AS total_expenses,
                    COUNT(*) AS transaction_count
                FROM transactions
                """
            ).fetchone()

        total_income = float(row["total_income"])
        total_expenses = float(row["total_expenses"])
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_balance": round(total_income - total_expenses, 2),
            "transaction_count": int(row["transaction_count"]),
        }

    def replace_all_transactions(self, transactions: list[Transaction]) -> int:
        with self._connect() as connection:
            connection.execute("DELETE FROM transactions")
            connection.executemany(
                """
                INSERT INTO transactions (
                    transaction_date,
                    entry_type,
                    category,
                    description,
                    amount,
                    payment_method,
                    reference,
                    notes,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        item.transaction_date,
                        item.entry_type,
                        item.category,
                        item.description,
                        round(float(item.amount), 2),
                        item.payment_method,
                        item.reference,
                        item.notes,
                        item.created_at,
                    )
                    for item in transactions
                ],
            )
        return len(transactions)
