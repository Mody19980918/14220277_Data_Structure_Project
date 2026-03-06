from dataclasses import dataclass


@dataclass(slots=True)
class Loan:
    book_name: str
    username: str
    due_date: str
    is_returned: bool
