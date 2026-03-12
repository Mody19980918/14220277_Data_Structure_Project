from typing import Iterable

from common.data_paths import loan_file_path
from models.loan import Loan


DELIMITER = "!=!=!"


def list_loans() -> list[Loan]:
    loans: list[Loan] = []
    try:
        with open(loan_file_path(), "r", encoding="utf-8") as file:
            for raw_line in file:
                line = raw_line.strip()
                if not line:
                    continue
                parts = line.split(DELIMITER)
                if len(parts) < 4:
                    continue
                # Data format:
                # book_name!=!=!username!=!=!due_date!=!=!is_returned
                if len(parts) == 4:
                    is_returned = parts[3].strip().lower() == "true"
                else:
                    is_returned = parts[4].strip().lower() == "true"
                loans.append(
                    Loan(
                        book_name=parts[0],
                        username=parts[1],
                        due_date=parts[2],
                        is_returned=is_returned,
                    )
                )
    except FileNotFoundError:
        return loans
    return loans


def append_loan(loan: Loan) -> None:
    is_returned = "True" if loan.is_returned else "False"
    with open(loan_file_path(), "a", encoding="utf-8") as file:
        file.write(
            f"{loan.book_name}{DELIMITER}{loan.username}{DELIMITER}{loan.due_date}{DELIMITER}{is_returned}\n"
        )


def overwrite_loans(loans: Iterable[Loan]) -> None:
    with open(loan_file_path(), "w", encoding="utf-8") as file:
        for loan in loans:
            is_returned = "True" if loan.is_returned else "False"
            file.write(
                f"{loan.book_name}{DELIMITER}{loan.username}{DELIMITER}{loan.due_date}{DELIMITER}{is_returned}\n"
            )
