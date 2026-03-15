from dataclasses import dataclass


@dataclass(slots=True)
class Loan:
    """
    Loan model
    """
    book_name: str
    username: str
    due_date: str
    is_returned: bool
