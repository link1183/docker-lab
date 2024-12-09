# SQLite-Flask User Management System

A modern web application for user management built with Flask and SQLite, containerized with Docker. The application provides a complete CRUD interface for managing users with separate development and production environments.

> 📚 **Documentation**: Check out our [Wiki](../../wiki) for comprehensive documentation:
>
> - [Installation Guide](../../wiki/Installation-Guide)
> - [User Guide](../../wiki/User-Guide)
> - [Development Guide](../../wiki/Development-Guide)
> - [Architecture Overview](../../wiki/Architecture-Overview)
> - [Troubleshooting](../../wiki/Troubleshooting)

## Table of Contents

1. [Features](#1-features)
2. [Architecture](#2-architecture)
   1. [Technical Stack](#21-technical-stack)
      - [Frontend](#frontend)
      - [Backend](#backend)
   2. [Environment-Specific Architecture](#22-environment-specific-architecture)
      - [Development Environment](#development-environment-app-dev)
      - [Production Environment](#production-environment-app-prod)
   3. [Docker Architecture](#23-docker-architecture)
      - [Container Structure](#container-structure)
      - [Shared Resources](#shared-resources)
   4. [Data Flow](#24-data-flow)
   5. [Security Considerations](#25-security-considerations)
3. [Prerequisites](#3-prerequisites)
4. [Setup](#4-setup)
   1. [Clone Repository](#41-clone-repository)
   2. [Build and Run](#42-build-and-run)
   3. [Access Application](#43-access-application)
   4. [Managing Application](#44-managing-application)
5. [Project Structure](#5-project-structure)
6. [Environment Variables](#6-environment-variables)
7. [Development](#7-development)
   1. [Database Initialization](#71-database-initialization)
   2. [Adding New Features](#72-adding-new-features)
8. [Troubleshooting](#8-troubleshooting)
   1. [Common Issues](#81-common-issues)
   2. [Getting Help](#82-getting-help)

## 1. Features

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
- **Modern UI/UX**:
  - Clean, responsive design
  - Modal dialogs for actions
  - Success/error notifications
  - Keyboard navigation support

## 2. Architecture

### 2.1 Technical Stack

#### Frontend

- **HTML5/CSS3**: Modern, responsive layouts using CSS Grid and Flexbox
- **JavaScript**: Pure vanilla JavaScript for dynamic interactions
- **Templates**: Jinja2 templating engine for server-side rendering
- **CSS Organization**:
  - `layout.css`: Core layout and structural styling
  - `components.css`: Reusable component styles
- **JavaScript Features**:
  - AJAX for asynchronous operations
  - Dynamic DOM updates
  - Modal management
  - Form handling
  - Real-time notifications

#### Backend

- **Flask**: Lightweight Python web framework
  - Route handling
  - Template rendering
  - Static file serving
- **SQLite**: File-based relational database
  - SQL schema management
  - Data persistence
  - Transaction support
- **Python Libraries**:
  - `sqlite3`: Database operations
  - `logging`: Application logging
  - `os`: Environment and path management

### 2.2 Environment-Specific Architecture

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

### 2.3 Docker Architecture

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

### 2.4 Data Flow

1. User interacts with frontend interface
2. JavaScript handles user actions
3. AJAX requests sent to Flask backend
4. Flask processes requests and interacts with SQLite
5. Results returned as JSON
6. Frontend updates dynamically with new data

### 2.5 Security Considerations

- Database files isolated in Docker volumes
- Environment-specific configurations
- Production-specific security measures:
  - Non-root user execution
  - Restricted file permissions
  - Minimal attack surface
- Input validation on both client and server
- SQL query parameterization
- Error handling and logging

[Previous remaining sections with added numbering...]

## 3. Prerequisites

Before you begin, ensure you have installed:

- Docker (version 20.10 or newer)
- Docker Compose (version 1.29 or newer)

## 4. Setup

### 4.1 Clone Repository

```sh
git clone https://github.com/link1183/docker-lab
cd docker-lab
```

### 4.2 Build and Run

```sh
docker compose up -d --build
```

### 4.3 Access Application

- Production: [http://localhost:8000](http://localhost:8000)
- Development: [http://localhost:8001](http://localhost:8001)

### 4.4 Managing Application

```sh
# Stop the application
docker compose down

# Stop and remove volumes
docker compose down -v

# View logs
docker compose logs -f app-dev app-prod
```

## 5. Project Structure

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

## 6. Environment Variables

The application uses these environment variables:

- `DB_PATH`: Path to the SQLite database file
- `ENV`: Environment type (`development` or `production`)
- `LOG_LEVEL`: Logging level (`DEBUG`, `INFO`, or `WARNING`)
- `SQL_FILE`: SQL file for database initialization

## 7. Development

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

## 8. Troubleshooting

### 8.1 Common Issues

1. **Modals not working:**

   - Check browser console for JavaScript errors
   - Verify that main.js is loaded properly

2. **Database errors:**

   - Ensure proper permissions on db directory
   - Check container logs for SQL errors
   - Verify SQL file syntax

3. **Container issues:**
   - Run `docker compose down -v` to clean state
   - Rebuild with `docker compose up -d --build`
   - Check logs with `docker compose logs`

### 8.2 Getting Help

If you encounter issues:

1. Check the application logs
2. Verify environment variables
3. Ensure all prerequisites are met
4. Clean and rebuild the containers
