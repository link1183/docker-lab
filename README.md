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
4. [Architecture](#4-architecture)
    1. [Technical Stack](#41-technical-stack)
        * [Frontend](#frontend)
        * [Backend](#backend)
    2. [Environment-Specific Architecture](#42-environment-specific-architecture)
        * [Development Environment](#development-environment-app-dev)
        * [Production Environment](#production-environment-app-prod)
    3. [Docker Architecture](#43-docker-architecture)
        * [Container Structure](#container-structure)
        * [Shared Resources](#shared-resources)
    4. [Data Flow](#44-data-flow)
    5. [Security Considerations](#45-security-considerations)
5. [Project Structure](#5-project-structure)
6. [Environment Variables](#6-environment-variables)
7. [Development](#7-development)
    1. [Database Initialization](#71-database-initialization)
    2. [Adding New Features](#72-adding-new-features)
8. [Troubleshooting](#8-troubleshooting)
    1. [Common Issues](#81-common-issues)
    2. [Getting Help](#82-getting-help)

## 1\. Prerequisites

Before you begin, ensure you have installed:

* [Docker](https://docs.docker.com/engine/install/)
* [Docker Compose](https://docs.docker.com/compose/)
* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## 2\. Setup

### 2.1 Clone Repository

``` sh
git clone https://github.com/link1183/docker-lab
cd docker-lab
```

### 2.2 Build and Run

``` sh
docker compose up -d --build
```

### 2.3 Access Application

* Production: [http://localhost:8000](http://localhost:8000)
* Development: [http://localhost:8001](http://localhost:8001)

### 2.4 Managing Application

``` sh
# Stop the application
docker compose down

# Stop and remove volumes
docker compose down -v

# View logs
docker compose logs -f app-dev app-prod
```

## 3\. Features

* **User Management Interface**:
    * View all users in a clean, responsive table
    * Add new users with a modal form
    * Edit existing users with pre-populated forms
    * Delete users with confirmation
* **Real-time Updates**:
    * AJAX-powered operations (no page refreshes)
    * Instant feedback with notifications
    * Dynamic table updates
* **Environment-Specific Configurations**:
    * Development environment optimized for debugging
    * Production environment optimized for performance and security

## 4\. Environment\-Specifics

#### 4.1 Launching server

We init our app with a bash script. In root folder it's init-db.sh file.
In development, we use exec the app.py file using:

``` python
python app.py
```

Flask output a message to told us not using this in production because it lunch a development server.
You can see this warning if you run ``docker compose up``:

> [!WARNING]
> app\-dev\-1 \| INFO:werkzeug:WARNING: This is a development server\. Do not use it in a production deployment\. Use a production WSGI server instead\.

In production we use Gunicorn to lunch our server. Gunicorn ist a python server for flasks app. In our case we init it in the init-db.sh:

``` sh
exec gunicorn --bind 0.0.0.0:8000 \
		--workers 4 \
		--access-logfile - \
		--error-logfile - \
		--capture-output \
		app:app
```

Gunicorn allows us to create workers to manage the tasks in queue. It's better when there's many people on the same app like in production.

#### 4.2 Environments vars

Each environment has is own vars. This vars are used to change db data, dependencies and frontend. They are listed in the docker-compose.yaml.

<br>
| DEV | PROD |
| --- | ---- |
| <span class="colour" style="color:rgb(191, 199, 213)"> </span><span class="colour" style="color:rgb(137, 221, 255)">environment</span><span class="colour" style="color:rgb(191, 199, 213)">:</span><br><span class="colour" style="color:rgb(191, 199, 213)">  - </span><span class="colour" style="color:rgb(191, 199, 213)">DB\_PATH=/app/db/dev-data.db</span><br><span class="colour" style="color:rgb(191, 199, 213)">  - </span><span class="colour" style="color:rgb(191, 199, 213)">ENV=development</span><br><span class="colour" style="color:rgb(191, 199, 213)">  - </span><span class="colour" style="color:rgb(191, 199, 213)">LOG\_LEVEL=DEBUG</span> | <span style="color: #bfc7d5;"> </span><span style="color: #89ddff;">environment</span><span style="color: #bfc7d5;">:</span><br><span style="color: #bfc7d5;">  - </span><span style="color: #bfc7d5;">DB\_PATH=/app/db/prod-data.db</span><br><span style="color: #bfc7d5;">  - </span><span style="color: #bfc7d5;">ENV=production</span><br><span style="color: #bfc7d5;">  - </span><span style="color: #bfc7d5;">LOG\_LEVEL=WARNING</span> |
<br>

#### 4.3 Datas

In dev, we try to break the system with specific data specials chars like é,.,`. You can see the list of the users in:[http://localhost:8000/users](http://localhost:8000/users)
In production, there's real data with "normal" names.

#### 4.4 Interface

There's some differences in the GUI. We display the title of the environment. It is not something you would do in a real context, but it is done here to give a visual distinction between the development and the production environnement.

#### 4.5 Log level

In development, we have to resolve a lot of problems so we logs most of the events. In production, we have less logs because the it would have no bug normally.
You can see this logs if you run the app not in background tasks ``docker composer up``

### 4.2 Environment-Specific Architecture

#### Development Environment (`app-dev`)

* **Server**: Flask Development Server
    * Built-in reloader
    * Detailed debugging information
    * Development-oriented error pages
* **Configuration**:
    * DEBUG level logging
    * Development-specific database with test data
    * Port 8001 exposed
* **Features**:
    * Extended error messages
    * Development-friendly debugging
    * Mock data for testing
    * Direct code execution

#### Production Environment (`app-prod`)

* **Server**: Gunicorn WSGI Server
    * 4 worker processes
    * Production-grade performance
    * Process management
    * Error handling
* **Security**:
    * Non-root user execution
    * Restricted permissions
    * Minimal dependencies
* **Configuration**:
    * WARNING level logging
    * Production database
    * Port 8000 exposed
    * Output capture for logging
* **Features**:
    * Optimized for performance
    * Process management
    * Load balancing
    * Production logging

### 4.3 Docker Architecture

#### Container Structure

1. **Base Image (Common)**:
    * Python 3.11 slim image
    * SQLite installation
    * Core dependencies
    * Application code
    * Static files and templates
2. **Development Specifics**:
    * Additional development dependencies
    * Mock data initialization
    * Flask development server
    * Debug-level logging
3. **Production Specifics**:
    * Gunicorn WSGI server
    * Production data initialization
    * Non-root user execution
    * Warning-level logging

#### Shared Resources

* **Volumes**:
    * `db-data`: Persistent storage for SQLite databases
    * Mounted at `/app/db` in both containers

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

* `DB_PATH`: Path to the SQLite database file
* `ENV`: Environment type (`development` or `production`)
* `LOG_LEVEL`: Logging level (`DEBUG`, `INFO`, or `WARNING`)
* `SQL_FILE`: SQL file for database initialization

## 7\. Development

### 7.1 Database Initialization

Database initialization happens at container startup:

* Development data is loaded from `db/dev-data.sql`
* Production data is loaded from `db/prod-data.sql`
* Data persists between container restarts via Docker volumes

### 7.2 Adding New Features

1. Frontend:
    * Templates are in `public/templates/`
    * CSS styles are split into layout and components
    * JavaScript handles all dynamic interactions
2. Backend:
    * Add new routes in `app.py`
    * Update SQL scripts in `db/` for new schemas
    * Follow the existing pattern for AJAX responses