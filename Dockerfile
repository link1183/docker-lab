# Stage 1: Base Image
FROM python:3.11-slim AS base

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Create a working directory
WORKDIR /app

# Copy application code and requirements
COPY ./app.py requirements.txt /app/
COPY ./public /app/public/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy init SCRIPT
COPY init.sh /app/
RUN chmod +x /app/init.sh

# Stage 2: Development Environment (Dev)
FROM base AS dev

# Install development dependencies
COPY requirements-dev.txt /app/requirements-dev.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy the dev SQL file and ensure permissions
COPY db/dev-data.sql /app/dev-data.sql
RUN chmod 644 /app/dev-data.sql

# Set environment variables for Dev
ENV SQL_FILE=dev-data.sql

# Create db directory with proper permissions
RUN mkdir -p /app/db && chmod 777 /app/db

# Command for the development environment
CMD ["/app/init.sh"]

# Stage 3: Production Environment
FROM base AS prod

# Copy the prod SQL file and ensure permissions
COPY db/prod-data.sql /app/prod-data.sql
RUN chmod 644 /app/prod-data.sql

# Set environment variables for Prod
ENV SQL_FILE=prod-data.sql

# Create db directory with proper permissions
RUN mkdir -p /app/db && chmod 777 /app/db

# Create a non-root user for security
RUN adduser --disabled-password --gecos '' appuser && \
  chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Use the init script which will handle both DB init and server startup
CMD ["/app/init.sh"]
