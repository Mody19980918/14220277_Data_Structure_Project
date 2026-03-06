from typing import Iterable

from common.data_paths import user_file_path
from models.user import User


DELIMITER = "!=!=!"


def list_users() -> list[User]:
    users: list[User] = []
    path = user_file_path()
    if not path:
        return users

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                clean_line = line.strip()
                if not clean_line:
                    continue
                split_params = clean_line.split(DELIMITER)
                if len(split_params) >= 2:
                    role = split_params[2] if len(split_params) > 2 else "user"
                    users.append(
                        User(username=split_params[0], password_hash=split_params[1], role=role)
                    )
    except FileNotFoundError:
        return users

    return users


def append_user(user: User) -> None:
    with open(user_file_path(), "a", encoding="utf-8") as file:
        file.write(f"{user.username}{DELIMITER}{user.password_hash}{DELIMITER}{user.role}\n")


def overwrite_users(users: Iterable[User]) -> None:
    with open(user_file_path(), "w", encoding="utf-8") as file:
        for user in users:
            file.write(f"{user.username}{DELIMITER}{user.password_hash}{DELIMITER}{user.role}\n")
