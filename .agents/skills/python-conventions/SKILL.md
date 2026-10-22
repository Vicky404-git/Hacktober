```markdown
---
name: python-conventions
description: Enforces Python coding standards, error handling patterns, and best practices for the repository.
---

# Python Conventions

## Overview

This skill ensures consistent, maintainable, and robust Python code across the repository. It defines guidelines for code structure, error handling, and common patterns.

## Entry Points

- `main.py`
- `pyproject.toml`

## Guidelines

### 1. Code Style
- Follow [PEP 8](https://peps.python.org/pep-0008/) standards.
- Use 4 spaces for indentation; no tabs.
- Keep lines under 88 characters to align with Black formatter defaults.
- Use snake_case for variables and functions, PascalCase for classes.
- Add docstrings to all public modules, classes, and functions.

### 2. Type Hinting
- Use type hints for all function arguments and return values.
- Import types from the `typing` module when necessary.
- Use `Optional` for nullable types.

### 3. Error Handling
- **Catch specific exceptions**; avoid bare `except` clauses.
- Log errors with context using the `logging` module.
- Raise custom exceptions for domain-specific errors.
- Ensure resources are properly cleaned up using `try/finally` or context managers.

### 4. Configuration
- Load configuration from environment variables or config files.
- Use `pyproject.toml` for project metadata and tool configurations.
- Separate configuration from business logic.

### 5. Testing
- Write unit tests in `tests/` directory.
- Use `pytest` as the testing framework.
- Aim for high test coverage, especially for critical paths.

## Error Handling Rules

1. **Specific Exceptions**: Always catch specific exceptions (e.g., `FileNotFoundError`, `ValueError`) rather than generic `Exception` or bare `except`.
2. **Logging**: Log errors with sufficient context (e.g., file paths, input values) using `logger.error()`.
3. **Re-raise**: If unable to handle an exception, re-raise it after logging.
4. **Custom Exceptions**: Define custom exception classes for domain-specific errors.
5. **Resource Cleanup**: Use `finally` blocks or context managers (`with` statement) to ensure resources are released.

## Standardized Code Examples

### Basic Function