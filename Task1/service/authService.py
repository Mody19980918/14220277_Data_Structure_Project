import bcrypt

from store import userStore as user_store
from models.user import User
from service.authError import AuthError


class AuthService:
    """
    Auth service
    """
    def register_user(self, username: str, password: str, role: str = "user") -> User:
        """
        Register a new user with username, password and role
        """
        clean_username = username.strip()
        if not clean_username:
            raise AuthError("Username cannot be blank.")
        if len(password) < 8:
            raise AuthError("Password must be at least 8 characters.")

        users = user_store.list_users()
        if any(user.username == clean_username for user in users):
            raise AuthError("Username already exists.")

        created_user = self.create_user(clean_username, password, role)
        return created_user

    def login(self, username: str, password: str) -> User:
        """
        Login a user with username and password
        """
        clean_username = username.strip()
        users = user_store.list_users()
        user = self.find_user(users, clean_username)
        if not user:
            raise AuthError("Invalid username or password.")

        is_valid = bcrypt.checkpw(
            password.encode("utf-8"), user.password_hash.encode("utf-8")
        )
        if not is_valid:
            raise AuthError("Invalid username or password.")
        return user

    def create_user(
        self, clean_username: str, password: str, role: str = "user"
    ) -> User:
        """
        Create a new user with username, password 
        """
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        created_user = User(
            username=clean_username,
            password_hash=password_hash,
            role=role,
        )
        user_store.append_user(created_user)
        return created_user

    def find_user(self, user: list[User], clean_username: str) -> User:
        """
        Find a user with username in the  user data base
        """
        users = user_store.list_users()
        for user in users:
            if user.username == clean_username:
                return user
        return None
