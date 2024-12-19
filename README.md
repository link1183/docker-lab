# SQLite-Flask User Management System

A modern web application for managing users, built with Flask and SQLite, featuring separate development and production environments. The system provides a complete CRUD interface within a Docker-containerized setup.

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

- Docker
- Docker Compose
- Git

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
