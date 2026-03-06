from dataclasses import dataclass


@dataclass(slots=True)
class Book:
    category: str
    name: str
    quantity: int
