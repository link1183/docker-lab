import os
import sqlite3
import logging
from flask import Flask, render_template, request, jsonify

# Set up logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="public/templates", static_folder="public/static")

# Database path
DB_PATH = os.getenv("DB_PATH")


def get_db_stats():
    """Get database statistics."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]

            try:
                db_size = os.path.getsize(DB_PATH)
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
        logger.error(f"Database error while getting stats: {e}")
        return {"total_users": "Error", "db_size": "Error"}


@app.route("/")
def welcome():
    """Enhanced home page with statistics."""
    logger.debug("Welcome page accessed.")
    stats = get_db_stats()
    return render_template(
        "home.html",
        stats=stats,
        env=os.getenv("ENV", "production"),
        success=request.args.get("success"),
        error=request.args.get("error"),
    )


@app.route("/users")
def get_users():
    """Enhanced user display page."""
    logger.debug("Fetching users from database.")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users")
            users = cursor.fetchall()

        return render_template(
            "users.html",
            users=users,
            env=os.getenv("ENV", "production"),
            success=request.args.get("success"),
            error=request.args.get("error"),
        )
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return render_template(
            "users.html",
            error="Failed to fetch users from the database",
            env=os.getenv("ENV", "production"),
        )


@app.route("/users/add", methods=["POST"])
def add_user():
    """Add a new user."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (request.form["name"], request.form["email"]),
            )
            conn.commit()

            # Fetch updated user list
            cursor.execute("SELECT id, name, email FROM users")
            users = cursor.fetchall()

        return jsonify({"message": "User added successfully", "users": users})
    except sqlite3.Error as e:
        logger.error(f"Database error while adding user: {e}")
        return jsonify({"error": "Failed to add user"}), 500


@app.route("/users/edit", methods=["POST"])
def edit_user():
    """Edit an existing user."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET name = ?, email = ? WHERE id = ?",
                (request.form["name"], request.form["email"], request.form["id"]),
            )
            conn.commit()

            # Fetch updated user list
            cursor.execute("SELECT id, name, email FROM users")
            users = cursor.fetchall()

        return jsonify({"message": "User updated successfully", "users": users})
    except sqlite3.Error as e:
        logger.error(f"Database error while updating user: {e}")
        return jsonify({"error": "Failed to update user"}), 500


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete a user."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()

            # Fetch updated user list
            cursor.execute("SELECT id, name, email FROM users")
            users = cursor.fetchall()

        return jsonify({"message": "User deleted successfully", "users": users})
    except sqlite3.Error as e:
        logger.error(f"Database error while deleting user: {e}")
        return jsonify({"error": "Failed to delete user"}), 500


if __name__ == "__main__":
    logger.info("Starting server...")
    app.run(host="0.0.0.0", port=8000)
