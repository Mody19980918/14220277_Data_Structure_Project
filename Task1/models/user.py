from dataclasses import dataclass


@dataclass(slots=True)
class User:
    username: str
    password_hash: str
    role: str = "user"
