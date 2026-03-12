from datetime import datetime, timedelta

from store import bookStore as book_store
from store import categoryStore as category_store
from store import loanStore as loan_store
from models.book import Book
from models.loan import Loan
from service.authError import BorrowError, ReturnError
import pandas as pd
import plotly.express as px


class UserPanelService:
    def home_summary(self, username: str) -> dict[str, object]:
        borrowed = self.list_borrowed_books(username)
        expired = self.list_expired_books(username)
        total_borrowed, borrowed_this_month, borrowed_this_week = (
            self.borrowing_activity_counts(username)
        )
        return {
            "borrowed_count": len(borrowed),
            "borrowed_names": [loan.book_name for loan in borrowed],
            "expired_count": len(expired),
            "expired_names": [loan.book_name for loan in expired],
            "has_expired": len(expired) > 0,
            "total_borrowed": total_borrowed,
            "borrowed_this_month": borrowed_this_month,
            "borrowed_this_week": borrowed_this_week,
        }

    def list_categories(self) -> list[str]:
        return category_store.list_categories()

    def list_available_books(self, category_id: str) -> list[Book]:
        books = book_store.list_books()
        return [
            book for book in books if book.category == category_id and book.quantity > 0
        ]

    def list_borrowed_books(self, user_id: str) -> list[Loan]:
        return [
            loan
            for loan in loan_store.list_loans()
            if loan.username == user_id and not loan.is_returned
        ]

    def borrowing_activity_counts(self, user_id: str) -> tuple[int, int, int]:
        user_loans = [loan for loan in loan_store.list_loans() if loan.username == user_id]
        total_borrowed = len(user_loans)

        current_time = datetime.now().date()
        week_start = current_time - timedelta(days=current_time.weekday())
        borrowed_this_month = 0
        borrowed_this_week = 0

        for loan in user_loans:
            try:
                due_date = datetime.strptime(loan.due_date, "%Y-%m-%d").date()
            except ValueError:
                continue
            borrowed_day = due_date - timedelta(days=30)
            if borrowed_day.year == current_time.year and borrowed_day.month == current_time.month:
                borrowed_this_month += 1
            if week_start <= borrowed_day <= current_time:
                borrowed_this_week += 1

        return total_borrowed, borrowed_this_month, borrowed_this_week

    def list_expired_books(self, user_id: str) -> list[Loan]:
        today = datetime.now().date()
        expired: list[Loan] = []
        for loan in self.list_borrowed_books(user_id):
            try:
                due = datetime.strptime(loan.due_date, "%Y-%m-%d").date()
            except ValueError:
                continue
            if due < today:
                expired.append(loan)
        return expired

    def daily_user_chart_html(self, user_id: str) -> str | None:
        """
        Return an HTML fragment with a Plotly chart showing the user's borrowing trend.
        Returns None if pandas/plotly not available or no data.
        """
        loans = [loan for loan in loan_store.list_loans() if loan.username == user_id]
        if not loans:
            return None

        current_time = datetime.now().date()
        daily_data: dict[str, dict[str, object]] = {}
        fine_per_book = 5.0
        for loan in loans:
            try:
                due_date = datetime.strptime(loan.due_date, "%Y-%m-%d").date()
            except ValueError:
                continue
            borrowed_day = (due_date - timedelta(days=30)).isoformat()
            row = daily_data.setdefault(
                borrowed_day, {"borrowed_books": 0, "is_unreturned": 0, "total_charges": 0.0}
            )
            row["borrowed_books"] = int(row["borrowed_books"]) + 1
            if not loan.is_returned:
                row["is_unreturned"] = int(row["is_unreturned"]) + 1
                if due_date < current_time:
                    row["total_charges"] = float(row["total_charges"]) + fine_per_book

        rows: list[dict[str, object]] = []
        for day, data in sorted(daily_data.items(), key=lambda item: item[0]):
            rows.append(
                {
                    "date": day,
                    "borrowed_books": int(data["borrowed_books"]),
                    "unreturned_count": int(data["is_unreturned"]),
                    "total_charges": float(data["total_charges"]),
                }
            )

        if not rows:
            return None

        df = pd.DataFrame(rows)
        trend_df = df.melt(
            id_vars=["date"],
            value_vars=["borrowed_books", "unreturned_count", "total_charges"],
            var_name="metric",
            value_name="value",
        )
        fig = px.line(trend_df, x="date", y="value", color="metric", markers=True, title="Your Borrowing Trend")
        fig.update_layout(template="plotly_white", margin={"l": 20, "r": 20, "t": 50, "b": 20}, legend_title_text="Metric")
        return fig.to_html(include_plotlyjs="cdn", full_html=False)

    def borrow_book(self, user_id: str, book_id: str) -> None:
        borrowed = self.list_borrowed_books(user_id)
        if len(borrowed) >= 3:
            raise BorrowError("You can borrow up to 3 books at the same time.")
        if any(loan.book_name == book_id for loan in borrowed):
            raise BorrowError("You have already borrowed this book.")
        if self.list_expired_books(user_id):
            raise BorrowError(
                "You have overdue books. Please contact admin for return and fine payment."
            )

        books = book_store.list_books()
        target = next((book for book in books if book.name == book_id), None)
        if not target or target.quantity <= 0:
            raise BorrowError("Book is not available now.")

        for book in books:
            if book.name == book_id:
                book.quantity -= 1
                break
        book_store.overwrite_books(books)

        due_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        loan_store.append_loan(
            Loan(book_name=book_id, username=user_id, due_date=due_date, is_returned=False)
        )

    def return_book(self, user_id: str, book_id: str) -> None:
        loans = loan_store.list_loans()
        current_time = datetime.now().date()
        target_index = next(
            (
                index
                for index, loan in enumerate(loans)
                if loan.username == user_id
                and loan.book_name == book_id
                and not loan.is_returned
            ),
            None,
        )
        if target_index is None:
            raise ReturnError("Cannot find this borrowed book.")

        target_loan = loans[target_index]
        try:
            due = datetime.strptime(target_loan.due_date, "%Y-%m-%d").date()
        except ValueError:
            due = None
        if due and due < current_time:
            raise ReturnError(
                "This book is overdue. Please contact admin to return it and pay fine."
            )

        loans[target_index].is_returned = True
        loan_store.overwrite_loans(loans)

        books = book_store.list_books()
        for book in books:
            if book.name == book_id:
                book.quantity += 1
                book_store.overwrite_books(books)
                return
