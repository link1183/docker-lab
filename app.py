import os
import sqlite3
import logging
from flask import Flask, jsonify, render_template_string

# Set up logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Database path
DB_PATH = os.getenv("DB_PATH", "/app/prod-data.db")

# HTML template for the welcome page
WELCOME_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>
</head>
<body>
    <h1>Welcome to the App!</h1>
    <p>Explore our app by visiting the <a href="/users">Users Page</a>.</p>
</body>
</html>
"""


@app.route("/")
def welcome():
    """Main page that links to the /users endpoint."""
    logger.debug("Welcome page accessed.")
    return render_template_string(WELCOME_PAGE)


@app.route("/users")
def get_users():
    """Fetch and return all users from the database."""
    logger.debug("Fetching users from database.")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users")
            users = cursor.fetchall()

        logger.debug("Users fetched successfully.")
        return jsonify(users)
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({"error": "Failed to fetch users from the database"}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


if __name__ == "__main__":
    logger.info("Starting server...")
    app.run(host="0.0.0.0", port=8000)
