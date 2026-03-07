class AuthError(Exception):
    """Authentication related errors."""
    pass
class BorrowError(Exception):
    """Borrow Book related errors."""
    pass
class ReturnError(Exception):
    """Return Book related errors."""
    pass