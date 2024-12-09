import os
import sqlite3
import logging
from flask import Flask, render_template_string

# Set up logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Database path
DB_PATH = os.getenv("DB_PATH", "/app/prod-data.db")

# HTML template with improved styling and visualization
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Management System</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .nav {
            margin-bottom: 20px;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 4px;
        }
        .nav a {
            color: #007bff;
            text-decoration: none;
        }
        .nav a:hover {
            text-decoration: underline;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background-color: #fff;
            padding: 15px;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .stat-card h3 {
            margin: 0;
            color: #6c757d;
            font-size: 0.9em;
            text-transform: uppercase;
        }
        .stat-card p {
            margin: 10px 0 0;
            font-size: 1.5em;
            color: #007bff;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background-color: white;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }
        th {
            background-color: #f8f9fa;
            font-weight: 600;
            color: #495057;
        }
        tr:hover {
            background-color: #f8f9fa;
        }
        .environment {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: 600;
        }
        .env-prod {
            background-color: #28a745;
            color: white;
        }
        .env-dev {
            background-color: #17a2b8;
            color: white;
        }
        .error-message {
            color: #dc3545;
            padding: 10px;
            background-color: #f8d7da;
            border-radius: 4px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>User Management System</h1>
        
        <div class="nav">
            <span class="environment {{ 'env-prod' if env == 'production' else 'env-dev' }}">
                {{ env.upper() }} Environment
            </span>
            | <a href="/">Home</a> | <a href="/users">View Users</a>
        </div>

        {% if page == 'home' %}
            <div class="stats">
                <div class="stat-card">
                    <h3>Total Users</h3>
                    <p>{{ stats.total_users }}</p>
                </div>
                <div class="stat-card">
                    <h3>Database Size</h3>
                    <p>{{ stats.db_size }}</p>
                </div>
                <div class="stat-card">
                    <h3>Environment</h3>
                    <p>{{ env.title() }}</p>
                </div>
            </div>
            <p>Welcome to the User Management System. You can view all users by clicking the "View Users" link above.</p>
        {% endif %}

        {% if page == 'users' %}
            {% if error %}
                <div class="error-message">{{ error }}</div>
            {% else %}
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Email</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for user in users %}
                        <tr>
                            <td>{{ user[0] }}</td>
                            <td>{{ user[1] }}</td>
                            <td>{{ user[2] }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% endif %}
        {% endif %}
    </div>
</body>
</html>
"""


def get_db_stats():
    """Get database statistics."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]

            # Get database file size
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
    return render_template_string(
        TEMPLATE, page="home", stats=stats, env=os.getenv("ENV", "production")
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

        logger.debug("Users fetched successfully.")
        return render_template_string(
            TEMPLATE, page="users", users=users, env=os.getenv("ENV", "production")
        )
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return render_template_string(
            TEMPLATE,
            page="users",
            error="Failed to fetch users from the database",
            env=os.getenv("ENV", "production"),
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return render_template_string(
            TEMPLATE,
            page="users",
            error="An unexpected error occurred",
            env=os.getenv("ENV", "production"),
        )


if __name__ == "__main__":
    logger.info("Starting server...")
    app.run(host="0.0.0.0", port=8000)
