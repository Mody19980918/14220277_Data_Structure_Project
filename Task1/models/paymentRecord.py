from dataclasses import dataclass


@dataclass(slots=True)
class PaymentRecord:
    """
    Payment record model
    """
    username: str
    amount: float
    paid_date: str
