PYTHON_BINARY := "python3"
VIRTUAL_ENV := "venv"
VIRTUAL_BIN := VIRTUAL_ENV / "bin"
PROJECT_NAME := "github_archive"
TEST_DIR := "test"

# Scans the project for security vulnerabilities
bandit:
    {{VIRTUAL_BIN}}/bandit -r {{PROJECT_NAME}}/

# Builds the project in preparation for release
build:
    {{VIRTUAL_BIN}}/python -m build

# Runs the Black Python formatter against the project
black:
    {{VIRTUAL_BIN}}/black {{PROJECT_NAME}}/ {{TEST_DIR}}/

# Checks if the project is formatted correctly against the Black rules
black-check:
    {{VIRTUAL_BIN}}/black {{PROJECT_NAME}}/ {{TEST_DIR}}/ --check

# Test the project and generate an HTML coverage report
coverage:
    {{VIRTUAL_BIN}}/pytest --cov={{PROJECT_NAME}} --cov-branch --cov-report=html --cov-report=lcov --cov-report=term-missing --cov-fail-under=90

# Cleans the project
clean:
    rm -rf {{VIRTUAL_ENV}} dist *.egg-info .coverage htmlcov .*cache
    find . -name '*.pyc' -delete

# Run flake8 checks against the project
flake8:
    {{VIRTUAL_BIN}}/flake8 {{PROJECT_NAME}}/ {{TEST_DIR}}/

# Lints the project
lint: black-check isort-check flake8 mypy bandit

# Runs all formatting tools against the project
lint-fix: black isort

# Install the project locally
install:
    {{PYTHON_BINARY}} -m venv {{VIRTUAL_ENV}}
    {{VIRTUAL_BIN}}/pip install -e ."[dev]"

# Sorts imports throughout the project
isort:
    {{VIRTUAL_BIN}}/isort {{PROJECT_NAME}}/ {{TEST_DIR}}/

# Checks that imports throughout the project are sorted correctly
isort-check:
    {{VIRTUAL_BIN}}/isort {{PROJECT_NAME}}/ {{TEST_DIR}}/ --check-only

# Run mypy type checking on the project
mypy:
    {{VIRTUAL_BIN}}/mypy {{PROJECT_NAME}}/ {{TEST_DIR}}/

# Scans the project for security vulnerabilities
scan:
    {{VIRTUAL_BIN}}/bandit -r {{PROJECT_NAME}}/

# Test the project
test:
    {{VIRTUAL_BIN}}/pytest
