Devs: Adrien Gunther, Claire Prodolliet, Thomas Burkhalter

# SQLite-Flask User Management System

A modern web application for managing users, built with Flask and SQLite, featuring separate development and production environments. The system provides a complete CRUD interface within a Docker-containerized setup.

## Table of Contents

1. [Quick Start](#quick-start)
   - [Prerequisites](#prerequisites)
   - [Basic Commands](#basic-commands)
2. [Core Features](#core-features)
3. [Development vs Production Environments](#development-vs-production-environments)
   - [Development Environment](#development-environment-port-8001)
   - [Production Environment](#production-environment-port-8000)
   - [Visual Distinctions](#visual-distinctions)
   - [Log Level Differences](#log-level-differences)
   - [Data Differences](#data-differences)
4. [Technical Architecture](#technical-architecture)
   - [Docker Container Structure](#docker-container-structure)
   - [Project Layout](#project-layout)
   - [Data Persistence](#data-persistence)
5. [Environment Configuration](#environment-configuration)
   - [Environment Variables](#environment-variables)
   - [Server Launch Methods](#server-launch-methods)
6. [Dependencies](#dependencies)
   - [Production Dependencies](#production-dependencies)
   - [Development Dependencies](#development-dependencies)
7. [Database Access](#database-access)
   - [Accessing Development Database](#accessing-development-database)
   - [Accessing Production Database](#accessing-production-database)
8. [Development Guide](#development-guide)
   - [Adding New Features](#adding-new-features)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/link1183/docker-lab
cd docker-lab

# Build and start containers
docker compose up -d --build

# Access the applications
Production: http://localhost:8000
Development: http://localhost:8001
```

### Prerequisites

- [Git](https://git-scm.com/downloads)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Basic Commands

```bash
# Stop containers
docker compose down

# Remove containers and volumes
docker compose down -v

# View application logs
docker compose logs -f app-dev    # Development logs
docker compose logs -f app-prod   # Production logs
```

## Core Features

- **Complete User Management**
  - View users in a responsive table
  - Add users through modal forms
  - Edit existing user information
  - Delete users with confirmation
  - Real-time updates via AJAX
  - Instant feedback notifications

## Development vs Production Environments

### Development Environment (Port 8001)

- **Server Configuration**

  - Flask Development Server
  - Hot-reloading enabled
  - DEBUG level logging
  - Extended error messages
  - Development database with test data
  - Direct code execution

- **Features**
  - Detailed debugging information
  - Development-oriented error pages
  - Mock data for testing
  - Special character testing in user data

### Production Environment (Port 8000)

- **Server Configuration**

  - Gunicorn WSGI Server
  - 4 worker processes
  - WARNING level logging
  - Production-grade database
  - Optimized performance settings

- **Security Features**
  - Non-root user execution
  - Restricted permissions
  - Minimal dependency set
  - Production-appropriate logging

### Visual Distinctions

- An environment variable is used to display the current environment on the frontend
- This visual indicator helps distinguish between development and production environments
- While not recommended for real production systems, it's implemented here for demonstration purposes
- The environment type can be verified by visiting:
  - Development: http://localhost:8001
  - Production: http://localhost:8000

### Log Level Differences

- **Development Environment**:

  - Extensive logging including access logs and debug information
  - View logs with: `docker compose logs app-dev -f`
  - Detailed error messages and stack traces
  - You'll see the Flask development server warning:
    ```
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
    ```

- **Production Environment**:
  - Minimal logging with only essential access logs
  - View logs with: `docker compose logs app-prod -f`
  - Production-appropriate error handling
  - Logs will show Gunicorn worker processes starting:
    ```
    [2024-xx-xx xx:xx:xx +0000] [xxx] [INFO] Starting gunicorn 20.x.x
    [2024-xx-xx xx:xx:xx +0000] [xxx] [INFO] Listening at: http://0.0.0.0:8000
    [2024-xx-xx xx:xx:xx +0000] [xxx] [INFO] Using worker: sync
    [2024-xx-xx xx:xx:xx +0000] [xxx] [INFO] Booting worker with pid: xxx
    ```

### Data Differences

- **Development**:
  - Contains test data with special characters (é, ., `)
  - Designed to test system robustness

The development data can be seen at [the following link](http://localhost:8001/users).

- **Production**:
  - Contains realistic user data
  - Uses standard character sets

The production data can be seen at [the following link](http://localhost:8000/users).

## Technical Architecture

### Docker Container Structure

```
Base Image (Python 3.11 slim)
├── Development Container
│   ├── Development dependencies
│   ├── Mock data
│   ├── Flask dev server
│   └── Debug logging
└── Production Container
    ├── Gunicorn server
    ├── Production data
    ├── Non-root user
    └── Warning-level logging
```

### Project Layout

```
.
├── app.py                 # Flask application
├── db/                    # Database files
│   ├── dev-data.sql      # Development data
│   └── prod-data.sql     # Production data
├── public/               # Frontend assets
│   ├── static/           # CSS and JavaScript
│   └── templates/        # Jinja2 templates
├── docker-compose.yml    # Docker configuration
└── Dockerfile           # Build instructions
```

### Data Persistence

- Docker volume `db-data` mounted at `/app/db`
- Separate databases for development and production
- Data persists between container restarts

## Environment Configuration

### Environment Variables

| Variable  | Description            | Values                      |
| --------- | ---------------------- | --------------------------- |
| DB_PATH   | Database file location | /app/db/dev-data.db (dev)   |
|           |                        | /app/db/prod-data.db (prod) |
| ENV       | Environment type       | development, production     |
| LOG_LEVEL | Logging verbosity      | DEBUG (dev), WARNING (prod) |
| SQL_FILE  | Initial data file      | dev-data.sql, prod-data.sql |

### Server Launch Methods

**Development:**

```bash
python app.py
```

**Production:**

```bash
exec gunicorn --bind 0.0.0.0:8000 \
    --workers 4 \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    app:app
```

## Dependencies

### Production Dependencies

(from `requirements.txt`)

- **Flask (3.1.0)**: Lightweight web framework for building the application
- **Gunicorn (23.0.0)**: Production-grade WSGI server for deploying Flask applications
- **Email-validator (2.2.0)**: Library for validating email addresses in user data
- **Bleach (6.2.0)**: Secure HTML sanitization library for cleaning user input

### Development Dependencies

(from `requirements-dev.txt`)

- **Pytest (8.3.4)**: Testing framework for writing and executing unit tests
- **Black (24.10.0)**: Code formatter to maintain consistent Python code style
- **Flake8 (7.1.1)**: Code linter that checks Python code for style and programming errors
- **Pylint (3.3.2)**: Static code analysis tool for checking code quality and finding errors

## Database Access

You can directly access and query the SQLite databases inside the containers. Each environment has its own database file.

### Accessing Development Database

1. Access the development container:

```bash
docker compose exec app-dev sh
```

2. Access the SQLite database:

```bash
sqlite3 /app/db/dev-data.db
```

### Accessing Production Database

1. Access the production container:

```bash
docker compose exec app-prod sh
```

2. Access the SQLite database:

```bash
sqlite3 /app/db/prod-data.db
```

### Useful SQLite Commands

Once in the SQLite prompt:

```sql
-- List all tables
.tables

-- Show table schema
.schema users

-- Make output prettier
.mode column
.headers on

-- Query examples
SELECT * FROM users;
SELECT * FROM users WHERE id = 1;

-- Exit SQLite
.quit
```

## Development Guide

### Adding New Features

1. **Frontend Development**

   - Add templates in `public/templates/`
   - Update CSS in `public/static/css/`
   - Implement JavaScript handlers for dynamic features

2. **Backend Development**

   - Add routes in `app.py`
   - Update database schemas in `db/`
   - Follow AJAX patterns for API responses

3. **Database Changes**
   - Modify initialization scripts in `db/`
   - Test changes in development environment first
   - Update both dev and prod SQL files as needed
