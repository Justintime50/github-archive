VIRTUAL_ENV := ".venv"
VIRTUAL_BIN := VIRTUAL_ENV / "bin"
PROJECT_NAME := "github_archive"
TEST_DIR := "test"

# Scans the project for security vulnerabilities
bandit:
    {{VIRTUAL_BIN}}/bandit -r {{PROJECT_NAME}}/

# Builds the project in preparation for release
build:
    {{VIRTUAL_BIN}}/python -m build

# Test the project and generate an HTML coverage report
coverage:
    {{VIRTUAL_BIN}}/pytest --cov={{PROJECT_NAME}} --cov-branch --cov-report=html --cov-report=lcov --cov-report=term-missing --cov-fail-under=90

# Cleans the project
clean:
    rm -rf {{VIRTUAL_ENV}} dist *.egg-info .coverage htmlcov .*cache
    find . -name '*.pyc' -delete

lint:
    {{VIRTUAL_BIN}}/ruff check {{PROJECT_NAME}}/ {{TEST_DIR}}/
    {{VIRTUAL_BIN}}/ruff format --check {{PROJECT_NAME}}/ {{TEST_DIR}}/

# Fixes lint issues
lint-fix:
    {{VIRTUAL_BIN}}/ruff check --fix {{PROJECT_NAME}}/ {{TEST_DIR}}/
    {{VIRTUAL_BIN}}/ruff format {{PROJECT_NAME}}/ {{TEST_DIR}}/

# Install the project locally
install:
    uv venv
    uv pip install -e '.[dev]'

# Run mypy type checking on the project
mypy:
    {{VIRTUAL_BIN}}/mypy --install-types --non-interactive {{PROJECT_NAME}}/ {{TEST_DIR}}/

# Test the project
test:
    {{VIRTUAL_BIN}}/pytest
