from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Iterable

from .models import Transaction
from .repositories import TransactionRepository


class AccountingService:
    CATEGORIES = [
        "Sales Revenue",
        "Operating Expense",
        "Supplier Payment",
        "Client Collection",
        "Payroll",
        "Utilities",
        "Tax",
        "Office Supplies",
        "Transport",
        "Other",
    ]

    PAYMENT_METHODS = ["Cash", "Bank Transfer", "Card", "Check", "Mobile Payment"]

    def __init__(self, repository: TransactionRepository, export_folder: Path) -> None:
        self.repository = repository
        self.export_folder = Path(export_folder)

    def build_transaction(self, form_data: dict, transaction_id: int | None = None) -> Transaction:
        amount = str(form_data.get("amount", "")).strip()
        return Transaction(
            id=transaction_id,
            transaction_date=str(form_data.get("transaction_date", "")).strip(),
            entry_type=str(form_data.get("entry_type", "")).strip(),
            category=str(form_data.get("category", "")).strip(),
            description=str(form_data.get("description", "")).strip(),
            amount=self._safe_amount(amount),
            payment_method=str(form_data.get("payment_method", "")).strip(),
            reference=str(form_data.get("reference", "")).strip(),
            notes=str(form_data.get("notes", "")).strip(),
        )

    def create_transaction(self, form_data: dict) -> tuple[bool, Transaction, list[str]]:
        transaction = self.build_transaction(form_data)
        errors = transaction.validate()
        if errors:
            return False, transaction, errors

        self.repository.create_transaction(transaction)
        return True, transaction, []

    def update_transaction(self, transaction_id: int, form_data: dict) -> tuple[bool, Transaction, list[str]]:
        transaction = self.build_transaction(form_data, transaction_id=transaction_id)
        errors = transaction.validate()
        if errors:
            return False, transaction, errors

        self.repository.update_transaction(transaction_id, transaction)
        return True, transaction, []

    def export_transactions(self, export_format: str) -> Path:
        transactions = self.repository.list_transactions()
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        export_path = self.export_folder / f"transactions-{timestamp}.{export_format}"

        if export_format == "json":
            export_path.write_text(json.dumps(transactions, indent=2), encoding="utf-8")
        elif export_format == "csv":
            with export_path.open("w", newline="", encoding="utf-8") as file_handle:
                writer = csv.DictWriter(file_handle, fieldnames=self.export_headers())
                writer.writeheader()
                writer.writerows(transactions)
        elif export_format == "txt":
            summary = self.repository.transaction_summary()
            lines = [
                "Accounting Activity Report",
                "=" * 28,
                f"Generated at: {datetime.now().isoformat(timespec='seconds')}",
                f"Total income: {summary['total_income']:.2f}",
                f"Total expenses: {summary['total_expenses']:.2f}",
                f"Net balance: {summary['net_balance']:.2f}",
                f"Transactions: {summary['transaction_count']}",
                "",
                "Detailed entries:",
            ]
            for row in transactions:
                lines.append(
                    f"- {row['transaction_date']} | {row['entry_type']} | {row['category']} | "
                    f"{row['description']} | {row['amount']:.2f} | {row['payment_method']}"
                )
            export_path.write_text("\n".join(lines), encoding="utf-8")
        else:
            raise ValueError("Unsupported export format.")

        return export_path

    def import_transactions(self, uploaded_file) -> tuple[int, list[str]]:
        filename = (uploaded_file.filename or "").lower()
        content = uploaded_file.read()

        try:
            if filename.endswith(".json"):
                records = json.loads(content.decode("utf-8"))
            elif filename.endswith(".csv"):
                decoded = content.decode("utf-8").splitlines()
                records = list(csv.DictReader(decoded))
            else:
                return 0, ["Only CSV and JSON imports are supported."]
        except (UnicodeDecodeError, json.JSONDecodeError, csv.Error, ValueError) as exc:
            return 0, [f"Import failed: {exc}"]

        if not isinstance(records, list):
            return 0, ["Imported file must contain a list of transaction records."]

        transactions: list[Transaction] = []
        errors: list[str] = []

        for index, record in enumerate(records, start=1):
            try:
                transaction = self._transaction_from_record(record)
            except ValueError as exc:
                errors.append(f"Row {index}: {exc}")
                continue

            validation_errors = transaction.validate()
            if validation_errors:
                errors.append(f"Row {index}: {' '.join(validation_errors)}")
                continue

            transactions.append(transaction)

        if errors:
            return 0, errors

        return self.repository.replace_all_transactions(transactions), []

    def _transaction_from_record(self, record: dict) -> Transaction:
        required_fields = {
            "transaction_date",
            "entry_type",
            "category",
            "description",
            "amount",
            "payment_method",
        }
        missing = sorted(field for field in required_fields if field not in record)
        if missing:
            raise ValueError(f"Missing fields: {', '.join(missing)}")

        return Transaction(
            transaction_date=str(record.get("transaction_date", "")).strip(),
            entry_type=str(record.get("entry_type", "")).strip(),
            category=str(record.get("category", "")).strip(),
            description=str(record.get("description", "")).strip(),
            amount=self._safe_amount(record.get("amount")),
            payment_method=str(record.get("payment_method", "")).strip(),
            reference=str(record.get("reference", "")).strip(),
            notes=str(record.get("notes", "")).strip(),
            created_at=str(record.get("created_at", "")).strip() or datetime.now().isoformat(timespec="seconds"),
        )

    @staticmethod
    def export_headers() -> Iterable[str]:
        return [
            "id",
            "transaction_date",
            "entry_type",
            "category",
            "description",
            "amount",
            "payment_method",
            "reference",
            "notes",
            "created_at",
        ]

    @staticmethod
    def _safe_amount(value) -> float:
        try:
            return float(value or 0)
        except (TypeError, ValueError):
            return 0.0
