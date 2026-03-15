from typing import Iterable

from common.data_paths import payment_file_path
from models.paymentRecord import PaymentRecord


DELIMITER = "!=!=!"


def list_payments() -> list[PaymentRecord]:
    """
    List all payments in the library
    """
    records: list[PaymentRecord] = []
    try:
        with open(payment_file_path(), "r", encoding="utf-8") as file:
            for raw_line in file:
                line = raw_line.strip()
                if not line:
                    continue
                parts = line.split(DELIMITER)
                if len(parts) < 3:
                    continue
                try:
                    amount = float(parts[1])
                except ValueError:
                    amount = 0.0
                records.append(
                    PaymentRecord(username=parts[0], amount=amount, paid_date=parts[2])
                )
    except FileNotFoundError:
        return records
    return records


def append_payment(record: PaymentRecord) -> None:
    """
    Append a payment to the library
    """
    with open(payment_file_path(), "a", encoding="utf-8") as file:
        file.write(f"{record.username}{DELIMITER}{record.amount}{DELIMITER}{record.paid_date}\n")


def overwrite_payments(records: Iterable[PaymentRecord]) -> None:
    """
    Overwrite the payments in the library
    """
    with open(payment_file_path(), "w", encoding="utf-8") as file:
        for record in records:
            file.write(
                f"{record.username}{DELIMITER}{record.amount}{DELIMITER}{record.paid_date}\n"
            )
