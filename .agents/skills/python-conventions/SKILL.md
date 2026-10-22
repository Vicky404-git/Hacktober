```markdown
---
name: python-conventions
description: Enforces PEP 8, type hints, error handling, and project structure standards for Python code in this repository.
---

# Python Conventions

## Overview

This skill ensures all Python code in this repository adheres to consistent style, structure, and error-handling practices. It applies to all `.py` files, with special attention to entry points `main.py` and configuration in `pyproject.toml`.

## Guidelines

### Code Style
- Follow **PEP 8** conventions strictly.
- Use **snake_case** for variables, functions, and module names.
- Use **PascalCase** for class names.
- Use **UPPER_SNAKE_CASE** for constants.
- Keep lines under **88 characters** (Black-compatible).
- Use **double quotes** for strings unless they contain double quotes.
- Include **docstrings** for all public modules, classes, and functions using the **Google style**.

### Type Hints
- All function signatures **must** include type hints for parameters and return types.
- Use `from __future__ import annotations` at the top of every module to enable forward references and improve readability.
- Use `Optional[T]` instead of `T | None` for broader Python version compatibility unless `pyproject.toml` specifies Python >= 3.10.
- Use `list[T]`, `dict[K, V]`, `tuple[T, ...]` instead of `List`, `Dict`, `Tuple` from `typing` (Python 3.9+).

### Project Structure
- Entry point: `main.py` must be the sole executable entry point.
- Configuration: All build, dependency, and tool settings live in `pyproject.toml`.
- Keep business logic in separate modules; `main.py` should only contain orchestration and CLI argument parsing.
- Avoid importing from `main.py` in other modules.

### Imports
- Group imports in this order:
  1. Standard library
  2. Third-party packages
  3. Local application modules
- Separate groups with a single blank line.
- Use absolute imports within the project.
- Avoid wildcard imports (`from module import *`).

### Logging
- Use the `logging` module, not `print()`, for all output in library code.
- Configure logging in `main.py