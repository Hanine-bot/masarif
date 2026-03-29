from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass(slots=True)
class Transaction:
    transaction_date: str
    entry_type: str
    category: str
    description: str
    amount: float
    payment_method: str
    reference: str = ""
    notes: str = ""
    id: int | None = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def validate(self) -> list[str]:
        errors: list[str] = []

        if self.entry_type not in {"income", "expense"}:
            errors.append("Entry type must be either income or expense.")

        if not self.category.strip():
            errors.append("Category is required.")

        if not self.description.strip():
            errors.append("Description is required.")

        if self.amount <= 0:
            errors.append("Amount must be greater than zero.")

        if not self.payment_method.strip():
            errors.append("Payment method is required.")

        try:
            date.fromisoformat(self.transaction_date)
        except ValueError:
            errors.append("Transaction date must use the YYYY-MM-DD format.")

        return errors

    def to_record(self) -> dict[str, object]:
        return {
            "id": self.id,
            "transaction_date": self.transaction_date,
            "entry_type": self.entry_type,
            "category": self.category,
            "description": self.description,
            "amount": round(float(self.amount), 2),
            "payment_method": self.payment_method,
            "reference": self.reference,
            "notes": self.notes,
            "created_at": self.created_at,
        }
