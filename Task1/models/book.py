from dataclasses import dataclass


@dataclass(slots=True)
class Book:
    """
    Book model
    """
    category: str
    name: str
    quantity: int
