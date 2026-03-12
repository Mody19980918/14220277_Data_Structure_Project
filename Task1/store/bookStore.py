from typing import Iterable

from common.data_paths import book_file_path
from models.book import Book


DELIMITER = "!=!=!"


def list_books() -> list[Book]:
    books: list[Book] = []
    try:
        with open(book_file_path(), "r", encoding="utf-8") as file:
            for raw_line in file:
                line = raw_line.strip()
                if not line:
                    continue
                parts = line.split(DELIMITER)
                if len(parts) < 3:
                    continue
                try:
                    quantity = int(parts[2])
                except ValueError:
                    quantity = 0
                books.append(Book(category=parts[0], name=parts[1], quantity=quantity))
    except FileNotFoundError:
        return books
    return books


def overwrite_books(books: Iterable[Book]) -> None:
    with open(book_file_path(), "w", encoding="utf-8") as file:
        for book in books:
            file.write(f"{book.category}{DELIMITER}{book.name}{DELIMITER}{book.quantity}\n")


def append_book(book: Book) -> None:
    with open(book_file_path(), "a", encoding="utf-8") as file:
        file.write(f"{book.category}{DELIMITER}{book.name}{DELIMITER}{book.quantity}\n")
