# SQLite-Flask User Management System

A modern web application for user management built with Flask and SQLite, containerized with Docker. The application provides a complete CRUD interface for managing users with separate development and production environments.

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Setup](#2-setup)
   1. [Clone Repository](#21-clone-repository)
   2. [Build and Run](#22-build-and-run)
   3. [Access Application](#23-access-application)
   4. [Managing Application](#24-managing-application)
3. [Features](#3-features)
4. [Environment-Specifics](#4-environment-specifics)
   1. [Launching Server](#41-launching-server)
   2. [Environment Variables](#42-environments-vars)
   3. [Data](#43-data)
   4. [Frontend](#44-frontend)
   5. [Log Level](#45-log-level)
5. [Environment-Specific Architecture](#5-environment-specific-architecture)
   1. [Development Environment](#51-development-environment-app-dev)
   2. [Production Environment](#52-production-environment-app-prod)
6. [Docker Architecture](#6-docker-architecture)
   1. [Container Structure](#61-container-structure)
   2. [Shared Resources](#62-shared-resources)
7. [Data Flow](#7-data-flow)
8. [Project Structure](#8-project-structure)
9. [Environment Variables](#9-environment-variables)
10. [Development](#10-development)
    1. [Database Initialization](#101-database-initialization)
    2. [Adding New Features](#102-adding-new-features)

## 1\. Prerequisites

Before you begin, ensure you have installed:

- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## 2\. Setup

### 2.1 Clone Repository

```sh
git clone https://github.com/link1183/docker-lab
cd docker-lab
```

### 2.2 Build and Run

```sh
docker compose up -d --build
```

### 2.3 Access Application

- Production: [http://localhost:8000](http://localhost:8000)
- Development: [http://localhost:8001](http://localhost:8001)

### 2.4 Managing Application

```sh
# Stop the application
docker compose down

# Stop and remove volumes
docker compose down -v

# View logs
docker compose logs -f app-dev app-prod
```

## 3\. Features

- **User Management Interface**:
  - View all users in a clean, responsive table
  - Add new users with a modal form
  - Edit existing users with pre-populated forms
  - Delete users with confirmation
- **Real-time Updates**:
  - AJAX-powered operations (no page refreshes)
  - Instant feedback with notifications
  - Dynamic table updates
- **Environment-Specific Configurations**:
  - Development environment optimized for debugging
  - Production environment optimized for performance and security

## 4\. Environment\-Specifics

#### 4.1 Launching server

The application is launched using the script `init.sh`.

In a development environnement (defined by the environnement variable `$ENV`), the server is launched using the following command:

```bash
python app.py
```

Running the command `python3 app.py` starts a Flask development server, which gives a warning.
You can see this warning if you run the command `docker compose logs app-dev -f`, or `docker compose up` if the containers aren't launched.

```
app-dev-1 | INFO:werkzeug:WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
```

In production we use Gunicorn, which is the official Flask production server, to launch our server.
Gunicorn allows us to define multiple parameters, such as the number of workers running.

```sh
exec gunicorn --bind 0.0.0.0:8000 \
		--workers 4 \
		--access-logfile - \
		--error-logfile - \
		--capture-output \
		app:app
```

#### 4.2 Environments vars

Each environment has is own variables. Those variables are used to change the data imported in the database, the dependencies, and some visual modifications on the frontend. They are listed in the file `docker-compose.yaml`.

| DEV                                                                                        | PROD                                                                                         |
| ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| environment:<br> - DB_PATH=/app/db/dev-data.db<br> - ENV=development<br> - LOG_LEVEL=DEBUG | environment:<br> - DB_PATH=/app/db/prod-data.db<br> - ENV=production<br> - LOG_LEVEL=WARNING |

#### 4.3 Data

In the development environment, we try to break the system with some specials chars like é,.,`.
In production, there's real data with "normal" names.

The list of users can be found at the following URL: [http://localhost:8000/users](http://localhost:8000/users)

#### 4.4 Frontend

An environnement variable is used to display the environment on the frontend. It is not something you would do in a real context, but it is done here to give a visual distinction between the development and the production environnements.

#### 4.5 Log level

In the development environment, it is important to give as many logs as possible, such as access logs, debugs logs and the likes. In the production environment, we don't need as many logs, so we only display the access logs.
Those logs can be seen with the command `docker compose logs app-prod -f` for the production environment, or `docker compose logs app-dev -f` for the development environment.

### 4.2 Environment-Specific Architecture

#### Development Environment (`app-dev`)

- **Server**: Flask Development Server
  - Built-in reloader
  - Detailed debugging information
  - Development-oriented error pages
- **Configuration**:
  - DEBUG level logging
  - Development-specific database with test data
  - Port 8001 exposed
- **Features**:
  - Extended error messages
  - Development-friendly debugging
  - Mock data for testing
  - Direct code execution

#### Production Environment (`app-prod`)

- **Server**: Gunicorn WSGI Server
  - 4 worker processes
  - Production-grade performance
  - Process management
  - Error handling
- **Security**:
  - Non-root user execution
  - Restricted permissions
  - Minimal dependencies
- **Configuration**:
  - WARNING level logging
  - Production database
  - Port 8000 exposed
  - Output capture for logging
- **Features**:
  - Optimized for performance
  - Process management
  - Load balancing
  - Production logging

### 4.3 Docker Architecture

#### Container Structure

1. **Base Image (Common)**:
   - Python 3.11 slim image
   - SQLite installation
   - Core dependencies
   - Application code
   - Static files and templates
2. **Development Specifics**:
   - Additional development dependencies
   - Mock data initialization
   - Flask development server
   - Debug-level logging
3. **Production Specifics**:
   - Gunicorn WSGI server
   - Production data initialization
   - Non-root user execution
   - Warning-level logging

#### Shared Resources

- **Volumes**:
  - `db-data`: Persistent storage for SQLite databases
  - Mounted at `/app/db` in both containers

### 4.4 Data Flow

1. User interacts with frontend interface
2. JavaScript handles user actions
3. AJAX requests sent to Flask backend
4. Flask processes requests and interacts with SQLite
5. Results returned as JSON
6. Frontend updates dynamically with new data

## 5\. Project Structure

```
.
├── app.py                 # Main Flask application
├── db/                    # Database files and SQL scripts
│   ├── dev-data.sql      # Development data initialization
│   └── prod-data.sql     # Production data initialization
├── public/               # Frontend assets
│   ├── static/           # Static files
│   │   ├── css/         # Stylesheets
│   │   └── js/          # JavaScript files
│   └── templates/        # Jinja2 templates
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile           # Multi-stage Docker build
└── requirements.txt     # Python dependencies
```

## 6\. Environment Variables

The application uses these environment variables:

- `DB_PATH`: Path to the SQLite database file
- `ENV`: Environment type (`development` or `production`)
- `LOG_LEVEL`: Logging level (`DEBUG`, `INFO`, or `WARNING`)
- `SQL_FILE`: SQL file for database initialization

## 7\. Development

### 7.1 Database Initialization

Database initialization happens at container startup:

- Development data is loaded from `db/dev-data.sql`
- Production data is loaded from `db/prod-data.sql`
- Data persists between container restarts via Docker volumes

### 7.2 Adding New Features

1. Frontend:
   - Templates are in `public/templates/`
   - CSS styles are split into layout and components
   - JavaScript handles all dynamic interactions
2. Backend:
   - Add new routes in `app.py`
   - Update SQL scripts in `db/` for new schemas
   - Follow the existing pattern for AJAX responses
