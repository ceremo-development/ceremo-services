# Ceremo Services

A Python Flask application built with clean architecture principles, featuring MySQL database integration and comprehensive development tooling.

## Features

- **MySQL Database**: Vitess MySQL cluster for scalable data storage
- **Clean Architecture**: Repositories and services pattern for maintainable code
- **Type Safety**: Type hints and Pydantic models for data validation
- **Error Handling**: Comprehensive error handling throughout the application
- **RESTful API**: Well-structured API endpoints
- **SQLAlchemy ORM**: Database operations with modern ORM

## Project Structure

```
ceremo-services/
├── app/
│   ├── contracts/       # Interface contracts and abstractions
│   ├── models/          # Domain Layer - Core business entities
│   ├── repositories/    # Infrastructure Layer - Data access
│   ├── routes/          # Interface Layer - API endpoints
│   ├── schemas/         # Data validation schemas
│   ├── services/        # Application Layer - Business logic
│   ├── utils/           # Utility functions and helpers
│   ├── config.py        # Application configuration
│   └── __init__.py
├── tests/
├── docker-compose.yml
├── .env.example
└── pyproject.toml
```

## Setup

### Prerequisites

- Python 3.11+
- Poetry
- Docker and Docker Compose (for Vitess)

### Installation

1. **Install dependencies:**
   ```bash
   poetry install
   ```

2. **Install pre-commit hooks:**
   ```bash
   poetry run pre-commit install
   ```

3. **Copy the environment file:**
   ```bash
   cp .env.example .env
   ```

4. **Update .env with your configuration**

## Running Locally

### Option 1: Using Docker Compose (Recommended)

Start the entire stack:
```bash
docker compose up -d
```

This will start:
- Vitess MySQL cluster (port 33577)
- Application server (port 5000)

### Option 2: Local Development

1. **Start Vitess database:**
   ```bash
   docker compose up -d vitess
   ```

2. **Wait for Vitess to be healthy:**
   ```bash
   docker compose ps
   ```

3. **Run database migrations:**
   ```bash
   flask db upgrade
   ```

4. **Start the application:**
   ```bash
   flask run
   ```

> **Note**: If you're using Poetry installed locally (e.g., via pipx), use `~/.local/bin/poetry` prefix for commands.

## Health Check

Check if the application and database are running:
```bash
python health_check.py http://localhost:5000
```

## Development

### Code Quality

This project uses pre-commit hooks to ensure code quality:

- **Black**: Code formatting
- **Flake8**: Linting and style guide enforcement
- **Bandit**: Security vulnerability scanning
- **MyPy**: Static type checking
- **Built-in hooks**: Trailing whitespace, end-of-file fixes, YAML validation

### Running Pre-commit Hooks

Pre-commit hooks run automatically on every commit. To run manually:

```bash
# Run on all files
poetry run pre-commit run --all-files

# Run on staged files only
poetry run pre-commit run

# Run specific hook
poetry run pre-commit run black
poetry run pre-commit run mypy
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test file
poetry run pytest tests/test_user_repository.py
```

### Manual Code Quality Checks

If you need to run tools individually:

```bash
# Code formatting
poetry run black app/

# Linting
poetry run flake8 app/

# Type checking
poetry run mypy app/

# Security scanning
poetry run bandit -r app/
```

## Architecture

### Clean Architecture Layers

- **Domain Layer** (`app/models/`): Core business entities and rules
- **Application Layer** (`app/services/`): Business logic and use cases
- **Infrastructure Layer** (`app/repositories/`): Data access and external services
- **Interface Layer** (`app/routes/`): API endpoints and controllers

### Key Design Patterns

- **Repository Pattern**: Data access abstraction
- **Dependency Injection**: Service layer dependencies
- **Generic Programming**: Type-safe base repository
- **Factory Pattern**: Database service initialization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and code quality checks
5. Submit a pull request

## License

MIT License
