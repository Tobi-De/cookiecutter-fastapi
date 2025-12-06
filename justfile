# List available commands
default:
    @just --list

# Install project dependencies
install:
    uv sync

# Run tests
test:
    uv run pytest tests/ -v

# Run tests with coverage
test-cov:
    uv run pytest tests/ --cov=. --cov-report=html --cov-report=term

# Generate a test project with default settings
generate-test:
    cookiecutter . --no-input project_name="Test Project"

# Generate a test project with Beanie database
generate-test-beanie:
    cookiecutter . --no-input project_name="Test Beanie Project" database="Beanie"

# Clean up generated test projects
clean:
    rm -rf test_project test_beanie_project

# Run pre-commit hooks on all files
lint:
    uv run pre-commit run --all-files

# Install pre-commit hooks
setup-hooks:
    uv run pre-commit install

# Build documentation
docs-build:
    cd docs && uv run make html

# Serve documentation locally
docs-serve:
    cd docs && uv run python -m http.server --directory _build/html 8000

# Run a quick validation (install, test, lint)
validate: install test lint

# Format code with black and isort
format:
    uv run black .
    uv run isort .
