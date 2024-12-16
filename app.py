import os
import sqlite3
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from flask import Flask, render_template, request, jsonify
from werkzeug.exceptions import HTTPException
from email_validator import validate_email, EmailNotValidError
from functools import wraps
import bleach


# Type definitions
@dataclass
class User:
    id: Optional[int]
    name: str
    email: str


class DatabaseError(Exception):
    pass


# Configuration
class Config:
    DB_PATH = os.getenv("DB_PATH", "users.db")
    ENV = os.getenv("ENV", "production")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    MAX_PER_PAGE = 100
    DEFAULT_PER_PAGE = 10


# Set up logging with more detailed configuration
def setup_logging() -> logging.Logger:
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(Config.LOG_LEVEL)
    return logger


logger = setup_logging()

app = Flask(__name__, template_folder="public/templates", static_folder="public/static")


# Database connection context manager
class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def __enter__(self) -> sqlite3.Connection:
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()


# Input validation
def validate_user_input(data: Dict) -> None:
    """Validate user input data."""
    if not data.get("name") or len(data["name"]) < 2:
        raise ValueError("Name must be at least 2 characters long")

    if not data.get("email"):
        raise ValueError("Email is required")

    try:
        validate_email(data["email"])
    except EmailNotValidError:
        raise ValueError("Invalid email format")


# Error handling decorator
def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Validation error: {str(e)}")
            return jsonify({"error": str(e)}), 400
        except DatabaseError as e:
            logger.error(f"Database error: {str(e)}")
            return jsonify({"error": "Database error occurred"}), 500
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return jsonify({"error": "An unexpected error occurred"}), 500

    return decorated_function


# Database operations
class UserRepository:
    @staticmethod
    def get_stats() -> Dict:
        """Get database statistics."""
        with Database(Config.DB_PATH) as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM users")
                total_users = tuple(cursor.fetchone())[0]  # Explicitly convert to tuple

                try:
                    db_size = os.path.getsize(Config.DB_PATH)
                    if db_size < 1024:
                        db_size = f"{db_size}B"
                    elif db_size < 1024 * 1024:
                        db_size = f"{db_size/1024:.1f}KB"
                    else:
                        db_size = f"{db_size/(1024*1024):.1f}MB"
                except OSError:
                    db_size = "Unknown"

                return {"total_users": total_users, "db_size": db_size}
            except sqlite3.Error as e:
                raise DatabaseError(f"Failed to get database stats: {e}")

    @staticmethod
    def get_users(page: int, per_page: int) -> Tuple[List[Tuple], int, int]:
        """Get paginated users."""
        with Database(Config.DB_PATH) as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM users")
                total_users = tuple(cursor.fetchone())[0]  # Explicitly convert to tuple

                offset = (page - 1) * per_page
                cursor.execute(
                    "SELECT id, name, email FROM users LIMIT ? OFFSET ?",
                    (per_page, offset),
                )
                # Explicitly convert each row to tuple
                users = [tuple(row) for row in cursor.fetchall()]

                total_pages = (total_users + per_page - 1) // per_page
                return users, total_pages, total_users
            except sqlite3.Error as e:
                raise DatabaseError(f"Failed to fetch users: {e}")

    @staticmethod
    def get_all_users() -> List[Tuple]:
        """Get all users."""
        with Database(Config.DB_PATH) as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, email FROM users")
                # Explicitly convert each row to tuple
                return [tuple(row) for row in cursor.fetchall()]
            except sqlite3.Error as e:
                raise DatabaseError(f"Failed to fetch users: {e}")

    @staticmethod
    def add_user(user_data: Dict) -> List[Tuple]:
        """Add a new user and return all users."""
        with Database(Config.DB_PATH) as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (name, email) VALUES (?, ?)",
                    (bleach.clean(user_data["name"]), bleach.clean(user_data["email"])),
                )
                conn.commit()
                return UserRepository.get_all_users()
            except sqlite3.Error as e:
                raise DatabaseError(f"Failed to add user: {e}")

    @staticmethod
    def update_user(user_id: int, user_data: Dict) -> List[Tuple]:
        """Update an existing user and return all users."""
        with Database(Config.DB_PATH) as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET name = ?, email = ? WHERE id = ?",
                    (
                        bleach.clean(user_data["name"]),
                        bleach.clean(user_data["email"]),
                        user_id,
                    ),
                )
                conn.commit()
                return UserRepository.get_all_users()
            except sqlite3.Error as e:
                raise DatabaseError(f"Failed to update user: {e}")

    @staticmethod
    def delete_user(user_id: int) -> List[Tuple]:
        """Delete a user and return all users."""
        with Database(Config.DB_PATH) as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
                return UserRepository.get_all_users()
            except sqlite3.Error as e:
                raise DatabaseError(f"Failed to delete user: {e}")


@app.route("/")
@handle_errors
def welcome():
    """Enhanced home page with statistics."""
    logger.debug("Welcome page accessed.")
    stats = UserRepository.get_stats()
    return render_template(
        "home.html",
        stats=stats,
        env=Config.ENV,
        success=request.args.get("success"),
        error=request.args.get("error"),
    )


# Routes
@app.route("/users")
@handle_errors
def get_users():
    """Get paginated list of users."""
    page = max(1, request.args.get("page", 1, type=int))
    per_page = min(
        max(1, request.args.get("per_page", Config.DEFAULT_PER_PAGE, type=int)),
        Config.MAX_PER_PAGE,
    )

    users, total_pages, total_users = UserRepository.get_users(page, per_page)

    if request.headers.get("Accept") == "application/json":
        return jsonify(
            {
                "users": users,
                "current_page": page,
                "total_pages": total_pages,
                "total_users": total_users,
            }
        )

    return render_template(
        "users.html",
        users=users,
        current_page=page,
        total_pages=total_pages,
        total_users=total_users,
        env=Config.ENV,
        success=request.args.get("success"),
        error=request.args.get("error"),
    )


@app.route("/users/add", methods=["POST"])
@handle_errors
def add_user():
    """Add a new user."""
    validate_user_input(request.form)
    users = UserRepository.add_user(request.form)
    return jsonify({"message": "User added successfully", "users": users})


@app.route("/users/edit", methods=["POST"])
@handle_errors
def edit_user():
    """Edit an existing user."""
    user_id = request.form.get("id", type=int)
    if not user_id:
        raise ValueError("User ID is required")

    validate_user_input(request.form)
    users = UserRepository.update_user(user_id, request.form)
    return jsonify({"message": "User updated successfully", "users": users})


@app.route("/users/<int:user_id>/delete", methods=["POST"])
@handle_errors
def delete_user(user_id):
    """Delete a user."""
    users = UserRepository.delete_user(user_id)
    return jsonify({"message": "User deleted successfully", "users": users})


# Error handlers
@app.errorhandler(HTTPException)
def handle_http_error(error):
    """Handle HTTP errors."""
    logger.error(f"HTTP error occurred: {error}")
    if request.headers.get("Accept") == "application/json":
        return jsonify({"error": str(error)}), error.code
    return render_template("error.html", error=error), error.code


if __name__ == "__main__":
    logger.info("Starting server...")
    app.run(host="0.0.0.0", port=8000)
