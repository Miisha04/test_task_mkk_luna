# Organizations API

A FastAPI-based REST API for managing organizations with PostgreSQL database and PostGIS support.

## Table of Contents

- [Organizations API](#organizations-api)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Running with Docker](#running-with-docker)
    - [Quick Start](#quick-start)
    - [Useful Docker Compose Commands](#useful-docker-compose-commands)
  - [Database Migrations](#database-migrations)
  - [API Endpoints](#api-endpoints)
  - [Environment Variables](#environment-variables)
  - [Development](#development)
    - [Local Development (without Docker)](#local-development-without-docker)
    - [Project Structure](#project-structure)
  - [Support](#support)

## Prerequisites

- Docker and Docker Compose installed on your system

## Running with Docker

### Quick Start

1. **Build and start the containers:**

```bash
docker compose up -d --build
```

This command will:
- Build the API image from the Dockerfile
- Start both the PostgreSQL database (with PostGIS extension) and FastAPI API server
- Run containers in detached mode (`-d` flag)
- Expose the API on `http://localhost:8000`
- Expose the database on `localhost:5432`

2. **Run database migrations:**

```bash
docker compose exec api uv run alembic upgrade head
```

This command applies all pending database migrations to set up the required schema.

3. **Verify the API is running:**

Open your browser or use curl to check the API:

```bash
curl http://localhost:8000/docs
```

This will display the interactive API documentation (Swagger UI).

### Useful Docker Compose Commands

- **Stop containers:**
  ```bash
  docker compose down
  ```

- **Stop and remove volumes (clean slate):**
  ```bash
  docker compose down -v
  ```

- **View logs:**
  ```bash
  docker compose logs -f api
  ```
  ```bash
  docker compose logs -f db
  ```

- **Access the database:**
  ```bash
  docker compose exec db psql -U postgres -d organizations
  ```

## Database Migrations

Migrations are managed using Alembic.

- **Create a new migration:**
  ```bash
  docker compose exec api uv run alembic revision --autogenerate -m "Description of changes"
  ```

- **Apply migrations:**
  ```bash
  docker compose exec api uv run alembic upgrade head
  ```

- **Rollback the last migration:**
  ```bash
  docker compose exec api uv run alembic downgrade -1
  ```

## API Endpoints

The API provides endpoints for managing organizations at `/organizations`.

- **Documentation:** http://localhost:8000/docs (Swagger UI)
- **ReDoc Documentation:** http://localhost:8000/redoc

All endpoints require an API key for authentication (see Environment Variables).

## Environment Variables

The following environment variables are configured in the `docker-compose.yml`:

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | db | Database host |
| `DB_PORT` | 5432 | Database port |
| `DB_USER` | postgres | Database user |
| `DB_PASSWORD` | postgres | Database password |
| `DB_NAME` | organizations | Database name |

**Note:** For production environments, update the database password and other sensitive variables in the `docker-compose.yml` file.

## Development

### Local Development (without Docker)

If you want to develop locally without Docker:

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```

2. Install dependencies:
   ```bash
   pip install uv
   uv sync
   ```

3. Set up your local database and run migrations:
   ```bash
   alembic upgrade head
   ```

4. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Project Structure

```
project/
├── app/
│   ├── models/          # SQLAlchemy models
│   ├── repositories/    # Data access layer
│   ├── routers/         # API route handlers
│   ├── schemas/         # Pydantic schemas for validation
│   ├── services/        # Business logic
│   ├── database.py      # Database configuration
│   ├── main.py          # FastAPI application entry point
│   └── security.py      # Authentication and security utilities
├── alembic/             # Database migrations
├── docker-compose.yml   # Docker Compose configuration
├── Dockerfile          # Docker image definition
└── pyproject.toml      # Project dependencies and metadata
```

## Support

For issues or questions, please check the logs:

```bash
docker compose logs api
```