#!/bin/bash

mkdir -p /app/db

if [ "$ENV" = "production" ]; then
	if [ ! -f "$DB_PATH" ] || [ ! "$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM users;")" -gt 0 ] 2>/dev/null; then
		echo "Initializing production database with initial data..."
		sqlite3 "$DB_PATH" <"/app/$SQL_FILE"
		echo "Production database initialized"
	else
		echo "Production database already exists with data"
	fi
else
	echo "Setting up development database schema..."
	sqlite3 "$DB_PATH" <"/app/$SQL_FILE"
	echo "Development database ready"
fi

# Start the application
exec python app.py
