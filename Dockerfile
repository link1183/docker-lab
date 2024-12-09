# Stage 1: Base Image
FROM python:3.11-slim AS base

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Create a working directory
WORKDIR /app

# Copy application code and requirements
COPY ./app.py requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Development Environment (Dev)
FROM base AS dev

# Install development dependencies (add dev packages here)
COPY requirements-dev.txt /app/requirements-dev.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy the dev SQL file
COPY db/dev-data.sql /app/dev-data.sql

# Execute the dev SQL file to create and populate the database
RUN sqlite3 /app/dev-data.db < /app/dev-data.sql && echo "SQL executed"

# Set environment variables for Dev
ENV ENV=dev
ENV LOG_LEVEL=DEBUG

# Command for the development environment
CMD ["python", "app.py"]

# Stage 3: Production Environment
FROM base AS prod

# Copy the prod SQL file
COPY db/prod-data.sql /app/prod-data.sql

# Execute the prod SQL file to create and populate the database
RUN sqlite3 /app/prod-data.db < /app/prod-data.sql && echo "SQL executed"

# Set environment variables for Prod
ENV ENV=production
ENV LOG_LEVEL=WARNING

# Command for the production environment
CMD ["python", "app.py"]
