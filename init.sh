#!/bin/bash

# Create database directory if it doesn't exist
mkdir -p /app/db

if [ "$ENV" = "production" ]; then
	echo "Initializing production database with initial data..."
	sqlite3 "$DB_PATH" <"/app/$SQL_FILE"
	echo "Production database initialized"

	# Start Gunicorn for production
	exec gunicorn --bind 0.0.0.0:8000 \
		--workers 4 \
		--access-logfile - \
		--error-logfile - \
		--capture-output \
		app:app
else
	echo "Setting up development database schema..."
	sqlite3 "$DB_PATH" <"/app/$SQL_FILE"
	echo "Development database ready"

	# Start Flask development server
	exec python app.py
fi
