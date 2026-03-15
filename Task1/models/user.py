from dataclasses import dataclass


@dataclass(slots=True)
class User:
    """
    User model
    """
    username: str  
    password_hash: str
    role: str = "user"
