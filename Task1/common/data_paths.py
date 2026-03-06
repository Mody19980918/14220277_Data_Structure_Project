import os

def get_data_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def user_file_path() -> str:
    return os.path.join(get_data_dir(), "../document/user.txt")


def category_file_path() -> str:
    return os.path.join(get_data_dir(), "../document/category.txt")


def book_file_path() -> str:
    return os.path.join(get_data_dir(), "../document/book.txt")


def loan_file_path() -> str:
    return os.path.join(get_data_dir(), "../document/borrowedBookDetail.txt")


def payment_file_path() -> str:
    return os.path.join(get_data_dir(), "../document/payment.txt")
