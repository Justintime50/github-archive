PYTHON_BINARY := python3
VIRTUAL_ENV := venv
VIRTUAL_BIN := $(VIRTUAL_ENV)/bin
PROJECT_NAME := github_archive
TEST_DIR := test

## help - Display help about make targets for this Makefile
help:
	@cat Makefile | grep '^## ' --color=never | cut -c4- | sed -e "`printf 's/ - /\t- /;'`" | column -s "`printf '\t'`" -t

## build - Builds the project in preparation for release
build:
	$(VIRTUAL_BIN)/python -m build

## coverage - Test the project and generate an HTML coverage report
coverage:
	$(VIRTUAL_BIN)/pytest --cov=$(PROJECT_NAME) --cov-branch --cov-report=html --cov-report=lcov --cov-report=term-missing

## clean - Remove the virtual environment and clear out .pyc files
clean:
	rm -rf $(VIRTUAL_ENV) dist *.egg-info .coverage
	find . -name '*.pyc' -delete

## black - Runs the Black Python formatter against the project
black:
	$(VIRTUAL_BIN)/black $(PROJECT_NAME)/ $(TEST_DIR)/

## black-check - Checks if the project is formatted correctly against the Black rules
black-check:
	$(VIRTUAL_BIN)/black $(PROJECT_NAME)/ $(TEST_DIR)/ --check

## format - Runs all formatting tools against the project
format: black isort lint mypy

## format-check - Checks if the project is formatted correctly against all formatting rules
format-check: black-check isort-check lint mypy

## install - Install the project locally
install:
	$(PYTHON_BINARY) -m venv $(VIRTUAL_ENV)
	$(VIRTUAL_BIN)/pip install -e ."[dev]"

## isort - Sorts imports throughout the project
isort:
	$(VIRTUAL_BIN)/isort $(PROJECT_NAME)/ $(TEST_DIR)/

## isort-check - Checks that imports throughout the project are sorted correctly
isort-check:
	$(VIRTUAL_BIN)/isort $(PROJECT_NAME)/ $(TEST_DIR)/ --check-only

## lint - Lint the project
lint:
	$(VIRTUAL_BIN)/flake8 $(PROJECT_NAME)/ $(TEST_DIR)/

## mypy - Run mypy type checking on the project
mypy:
	$(VIRTUAL_BIN)/mypy $(PROJECT_NAME)/ $(TEST_DIR)/

## scan - Scans the project for security vulnerabilities
scan:
	$(VIRTUAL_BIN)/bandit -r $(PROJECT_NAME)/

## test - Test the project
test:
	$(VIRTUAL_BIN)/pytest

.PHONY: help build coverage clean black black-check format format-check install isort isort-check lint mypy scan test
