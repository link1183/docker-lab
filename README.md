# SQLite-Flask User Management System

A modern web application for user management built with Flask and SQLite, containerized with Docker. The application provides a complete CRUD interface for managing users with separate development and production environments.

## Features

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

## Architecture

### Technical Stack

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

### Environment-Specific Architecture

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

### Docker Architecture

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

### Data Flow

1. User interacts with frontend interface
2. JavaScript handles user actions
3. AJAX requests sent to Flask backend
4. Flask processes requests and interacts with SQLite
5. Results returned as JSON
6. Frontend updates dynamically with new data

### Security Considerations

- Database files isolated in Docker volumes
- Environment-specific configurations
- Production-specific security measures:
  - Non-root user execution
  - Restricted file permissions
  - Minimal attack surface
- Input validation on both client and server
- SQL query parameterization
- Error handling and logging

## Prerequisites

Before you begin, ensure you have installed:

- Docker (version 20.10 or newer)
- Docker Compose (version 1.29 or newer)

## Setup

### 1. Clone the repository

```sh
git clone https://github.com/link1183/docker-lab
cd docker-lab
```

### 2. Build and run with Docker Compose

```sh
docker compose up -d --build
```

This command will:

- Build images for both environments
- Create and start the containers
- Mount necessary volumes for database persistence
- Expose the following ports:
  - Production Environment: [http://localhost:8000](http://localhost:8000)
  - Development Environment: [http://localhost:8001](http://localhost:8001)

### 3. Access the Application

- Production: [http://localhost:8000](http://localhost:8000)
- Development: [http://localhost:8001](http://localhost:8001)

Each environment provides:

- Dashboard with environment info and statistics
- Complete user management interface
- Separate database instance

### 4. Managing the Application

**Stop the application:**

```sh
docker compose down
```

**Stop and remove volumes (cleans database):**

```sh
docker compose down -v
```

**View logs:**

```sh
docker compose logs -f app-dev app-prod
```

## Project Structure

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

## Environment Variables

The application uses these environment variables:

- `DB_PATH`: Path to the SQLite database file
- `ENV`: Environment type (`development` or `production`)
- `LOG_LEVEL`: Logging level (`DEBUG`, `INFO`, or `WARNING`)
- `SQL_FILE`: SQL file for database initialization

## Development

### Database Initialization

Database initialization happens at container startup:

- Development data is loaded from `db/dev-data.sql`
- Production data is loaded from `db/prod-data.sql`
- Data persists between container restarts via Docker volumes

### Adding New Features

1. Frontend:

   - Templates are in `public/templates/`
   - CSS styles are split into layout and components
   - JavaScript handles all dynamic interactions

2. Backend:
   - Add new routes in `app.py`
   - Update SQL scripts in `db/` for new schemas
   - Follow the existing pattern for AJAX responses

## Troubleshooting

### Common Issues

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

### Getting Help

If you encounter issues:

1. Check the application logs
2. Verify environment variables
3. Ensure all prerequisites are met
4. Clean and rebuild the containers

## License

This project is licensed under the MIT License - see the LICENSE file for details.
