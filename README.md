# SQLite-Flask Dockerized App

This project is a simple Python-based web server using Flask and SQLite, dockerized to run both a Test Environment (with mock data) and a Production Environment (with real data). The app serves two endpoints:

- A welcome page at `/` with a link to view users.
- An endpoint `/users` that retrieves all users from the SQLite database in JSON format.

## Features

- **Welcome Page**: A simple page that links to the `/users` endpoint.
- **Users Endpoint**: The `/users` endpoint retrieves users from the database (Test or Production) and returns them in JSON format.
- **Multiple Environments**: Test environment with mock data and Production environment with real data.

## Prerequisites

Before you begin, ensure that you have the following installed:

- Docker (version 20.10 or newer)
- Docker Compose (version 1.29 or newer)

## Setup

### 1. Clone the repository

First, clone the repository to your local machine:

```sh
git clone <repository-url>
cd <repository-directory>
```

### 2. Build and run with Docker Compose

You can build and run the app with Docker Compose. This will create and start both the test and production containers.

```sh
docker-compose up --build
```

This command will:

- Build the images for both test and production environments.
- Set up and start containers for both environments.
- Expose the following ports:
  - Test Environment: [http://localhost:8001](http://localhost:8001) (mock data).
  - Production Environment: [http://localhost:8000](http://localhost:8000) (real data).

### 3. Access the App

- Visit [http://localhost:8000](http://localhost:8000) for the production environment.
- Visit [http://localhost:8001](http://localhost:8001) for the test environment.

Both environments will show the same welcome page with a link to view users.

### 4. Stopping the App

To stop the running containers, use the following command:

```sh
docker-compose down
```

This will stop and remove the containers, networks, and volumes created by Docker Compose.

## Dockerfile Breakdown

This project uses a multi-stage Dockerfile to create separate environments for Test and Production:

- **Base Image**:

  - Installs Python 3.11, SQLite, and app dependencies.
  - Copies the Flask app code and the `requirements.txt` file.

- **Test Environment**:

  - Creates a SQLite database (`test.db`) with mock data for testing purposes.
  - Sets the environment variable `ENV=test` and points to the `test.db` file.

- **Production Environment**:
  - Creates a SQLite database (`prod.db`) with real data.
  - Sets the environment variable `ENV=production` and points to the `prod.db` file.

## Environment Variables

The application uses the following environment variables:

- `DB_PATH`: Path to the SQLite database file. Default is `test.db` (for test environment).
- `ENV`: The environment type. Can be either `test` or `production`.
- `LOG_LEVEL`: Logging level. Set this to `DEBUG`, `INFO`, or `ERROR`.

## Troubleshooting

- **App not starting?** Ensure that Docker and Docker Compose are installed correctly, and try rebuilding the images with `docker-compose up --build`.
- **Database connection errors?** Verify that the environment variables are set correctly and that the database files are accessible.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
