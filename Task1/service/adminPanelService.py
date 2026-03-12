from datetime import date, datetime, timedelta
import pandas as pd
import plotly.express as px


from store import bookStore as book_store
from store import categoryStore as category_store
from store import loanStore as loan_store
from store import paymentStore as payment_store
from store import userStore as user_store
from models.book import Book
from models.paymentRecord import PaymentRecord

class AdminPanelService:
    FINE_PER_BOOK = 5.0

    def today_statistics(self) -> dict[str, int | float]:
        today = datetime.now().date()
        loans = loan_store.list_loans()

        users_rented_today: set[str] = set()
        users_need_to_pay: set[str] = set()
        unpaid_expired_count = 0

        for loan in loans: 
            due_date = self._parse_date(loan.due_date)
            if due_date:
                borrowed_day = due_date - timedelta(days=30)
                if borrowed_day == today:
                    users_rented_today.add(loan.username)
                if due_date < today and not loan.is_returned:
                    users_need_to_pay.add(loan.username)
                    unpaid_expired_count += 1

        return {
            "students_rented_today": len(users_rented_today),
            "students_need_to_pay": len(users_need_to_pay),
            "total_expired_charges": unpaid_expired_count * self.FINE_PER_BOOK,
        }

    def find_user_fines(self, username: str) -> dict[str, int | float | str | bool]:
        clean_username = username.strip()
        if not clean_username:
            return {"username": "", "count": 0, "amount": 0.0, "found": False}

        users = user_store.list_users()
        if not any(user.username == clean_username for user in users):
            return {
                "username": clean_username,
                "count": 0,
                "amount": 0.0,
                "found": False,
            }

        today = datetime.now().date()
        loans = loan_store.list_loans()
        overdue_count = 0
        for loan in loans:
            due_date = self._parse_date(loan.due_date)
            if (
                loan.username == clean_username
                and due_date
                and due_date < today
                and not loan.is_returned
            ):
                overdue_count += 1

        return {
            "username": clean_username,
            "count": overdue_count,
            "amount": overdue_count * self.FINE_PER_BOOK,
            "found": True,
        }

    def mark_fines_as_paid(self, user_id: str) -> int:
        clean_user_id = user_id.strip()
        if not clean_user_id:
            return 0

        today = datetime.now().date()
        loans = loan_store.list_loans()
        updated_count = 0
        total_paid = 0.0
        for loan in loans:
            due_date = self._parse_date(loan.due_date)
            if (
                loan.username == clean_user_id
                and due_date
                and due_date < today
                and not loan.is_returned
            ):
                loan.is_returned = True
                updated_count += 1
                total_paid += self.FINE_PER_BOOK
        if updated_count:
            loan_store.overwrite_loans(loans)
            payment_store.append_payment(
                PaymentRecord(
                    username=clean_user_id,
                    amount=total_paid,
                    paid_date=today.isoformat(),
                )
            )
        return updated_count

    def add_book(self, category: str, book_name: str, quantity: int) -> Book:
        clean_category = category.strip()
        clean_book_name = book_name.strip()
        if not clean_category:
            raise ValueError("Category cannot be blank.")
        if not clean_book_name:
            raise ValueError("Book name cannot be blank.")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")

        books = book_store.list_books()
        existing = next((book for book in books if book.name == clean_book_name), None)
        if existing:
            existing.quantity += quantity
            book_store.overwrite_books(books)
            return existing

        created = Book(category=clean_category, name=clean_book_name, quantity=quantity)
        book_store.append_book(created)

        categories = category_store.list_categories()
        if clean_category not in categories:
            category_store.append_category(clean_category)
        return created

    def list_categories(self) -> list[str]:
        return category_store.list_categories()

    def list_book_names(self) -> list[str]:
        return [book.name for book in book_store.list_books()]

    def list_books_by_category(self, category: str) -> list[Book]:
        return [book for book in book_store.list_books() if book.category == category]

    def list_deletable_usernames(self) -> list[str]:
        return [user.username for user in user_store.list_users() if user.role != "admin"]

    def add_category(self, category: str) -> str:
        clean_category = category.strip()
        if not clean_category:
            raise ValueError("Category cannot be blank.")
        categories = category_store.list_categories()
        if clean_category in categories:
            raise ValueError("Category already exists.")
        category_store.append_category(clean_category)
        return clean_category

    def delete_book(self, book_name: str) -> str:
        clean_book_name = book_name.strip()
        if not clean_book_name:
            raise ValueError("Book name cannot be blank.")

        loans = loan_store.list_loans()
        if any(
            loan.book_name == clean_book_name and not loan.is_returned for loan in loans
        ):
            raise ValueError("Cannot delete book with active borrowed records.")

        books = book_store.list_books()
        if not any(book.name == clean_book_name for book in books):
            raise ValueError("Book not found.")

        filtered_books = [book for book in books if book.name != clean_book_name]
        book_store.overwrite_books(filtered_books)
        return clean_book_name

    def delete_category(self, category: str) -> str:
        clean_category = category.strip()
        if not clean_category:
            raise ValueError("Category cannot be blank.")

        categories = category_store.list_categories()
        if clean_category not in categories:
            raise ValueError("Category not found.")

        books = book_store.list_books()
        if any(book.category == clean_category for book in books):
            raise ValueError("Cannot delete category while books still belong to it.")

        filtered_categories = [item for item in categories if item != clean_category]
        category_store.overwrite_categories(filtered_categories)
        return clean_category

    def delete_user_account(self, username: str) -> str:
        clean_username = username.strip()
        if not clean_username:
            raise ValueError("Username cannot be blank.")

        users = user_store.list_users()
        target_user = None
        for user in users:
            if user.username == clean_username:
                target_user = user
                break
        if target_user is None:
            raise ValueError("User not found.")
        if target_user.role == "admin":
            raise ValueError("Cannot delete admin account.")

        loans = loan_store.list_loans()
        if any(loan.username == clean_username and not loan.is_returned for loan in loans):
            raise ValueError("Cannot delete user with unreturned books.")

        remaining_users = [user for user in users if user.username != clean_username]
        user_store.overwrite_users(remaining_users)
        return clean_username

    def daily_trend_chart(self) -> str | None:

        loans = loan_store.list_loans()
        today = datetime.now().date()

        # Initialize daily data for last 7 days
        daily_data: dict[str, dict[str, object]] = {}
        for i in range(7):
            day = (today - timedelta(days=i)).isoformat()
            daily_data[day] = {
                "borrowed_books": 0,
                "unreturned_students": set(),
                "total_charges": 0.0
            }

        for loan in loans:
            due_date = self._parse_date(loan.due_date)
            if not due_date:
                continue
            borrowed_day = (due_date - timedelta(days=30)).isoformat()

            # Skip if borrowed day is not in our 7-day window
            if borrowed_day not in daily_data:
                continue

            row = daily_data[borrowed_day]
            row["borrowed_books"] = int(row["borrowed_books"]) + 1
            if not loan.is_returned:
                unreturned_users = row["unreturned_students"]
                if isinstance(unreturned_users, set):
                    unreturned_users.add(loan.username)
                if due_date < today:
                    row["total_charges"] = float(row["total_charges"]) + self.FINE_PER_BOOK

        rows: list[dict[str, int | float | str]] = []
        for day, data in sorted(daily_data.items(), key=lambda item: item[0]):
            users = data["unreturned_students"]
            unreturned_count = len(users) if isinstance(users, set) else 0
            rows.append(
                {
                    "date": day,
                    "borrowed_books": int(data["borrowed_books"]),
                    "unreturned_students": unreturned_count,
                    "total_charges": float(data["total_charges"]),
                }
            )

        if not rows:
            return None

        dataframe = pd.DataFrame(rows)
        trend_df = dataframe.melt(
            id_vars=["date"],
            value_vars=["borrowed_books", "unreturned_students", "total_charges"],
            var_name="metric",
            value_name="value",
        )
        fig = px.line(
            trend_df,
            x="date",
            y="value",
            color="metric",
            markers=True,
            title="Daily Library Trend",
        )
        fig.update_layout(
            template="plotly_white",
            margin={"l": 20, "r": 20, "t": 50, "b": 20},
            legend_title_text="Metric",
        )
        return fig.to_html(include_plotlyjs="cdn", full_html=False)

    def _parse_date(self, raw_date: str) -> date | None:
        try:
            return datetime.strptime(raw_date, "%Y-%m-%d").date()
        except ValueError:
            return None
