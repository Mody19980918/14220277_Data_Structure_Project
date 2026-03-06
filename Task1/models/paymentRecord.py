from dataclasses import dataclass


@dataclass(slots=True)
class PaymentRecord:
    username: str
    amount: float
    paid_date: str
