```markdown
---
name: python-conventions
description: Enforces PEP 8, type hints, docstrings, and error handling standards for Python code in this repository.
---

# Python Conventions

## Guidelines

### Code Style
- Follow **PEP 8** formatting rules.
- Use 4 spaces for indentation (no tabs).
- Maximum line length: **88 characters** (Black-compatible).
- Import order: standard library → third-party → local, separated by blank lines.
- Use **snake_case** for functions, variables, and methods.
- Use **PascalCase** for classes.
- Use **UPPER_SNAKE_CASE** for constants.

### Type Hints
- All function signatures must include type hints for parameters and return values.
- Use modern type hint syntax (e.g., `list[str]` instead of `List[str]` for Python 3.9+).
- Optional parameters must be annotated (e.g., `str | None`).

### Docstrings
- All public functions, methods, and classes must have a **Google-style docstring**.
- Include:
  - A short summary line.
  - `Args:` section for parameters.
  - `Returns:` section for return values.
  - `Raises:` section for exceptions.
  - `Examples:` section with usage.

### Error Handling
- **Never** use bare `except:` clauses.
- Catch specific exceptions (e.g., `ValueError`, `FileNotFoundError`).
- Log errors using the `logging` module (not `print`).
- Raise custom exceptions for domain-specific errors when appropriate.
- Use `raise ... from e` to preserve exception chaining.
- Validate inputs at function boundaries and raise `ValueError` or `TypeError` for invalid arguments.

### Project Structure
- Entry points: `main.py` is the primary executable script.
- Project metadata and dependencies are defined in `pyproject.toml`.
- Keep `main.py` thin; delegate logic to well-structured modules.

## Standardized Code Examples

### Basic Function with Type Hints and Docstring

```python
def calculate_average(numbers: list[float]) -> float:
    """Calculate the arithmetic mean of a list of numbers.

    Args:
        numbers: A non-empty list of floating-point numbers.

    Returns:
        The arithmetic mean of the input numbers.

    Raises:
        ValueError: If the input list is empty.

    Examples:
        >>> calculate_average([1.0, 2.0, 3.0])
        2.0
    """
    if not numbers:
        raise ValueError("Cannot calculate average of an empty list")
    return sum(numbers) / len(numbers)
```

### Error Handling with Logging

```python
import logging

logger = logging.getLogger(__name__)

def read_config(filepath: str) -> dict[str, str]:
    """Read configuration from a file.

    Args:
        filepath: Path to the configuration file.

    Returns:
        A dictionary of configuration key-value pairs.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be read due to permissions.

    Examples:
        >>> config = read_config("config.ini")
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return {line.split(":")[0].strip(): line.split(":")[1].strip()
                    for line in f if ":" in line}
    except FileNotFoundError as e:
        logger.error("Config file not found: %s", filepath)
        raise
    except PermissionError as e:
        logger.error("Permission denied reading config: %s", filepath)
        raise
```

### Class with Type Hints

```python
class DataProcessor:
    """Process raw data into standardized format.

    Attributes:
        buffer: Internal buffer for accumulating processed items.
    """

    def __init__(self, threshold: float = 0.5) -> None:
        """Initialize the processor with a filtering threshold.

        Args:
            threshold: Minimum value for filtering data points.
        """
        self.threshold = threshold
        self.buffer: list[float] = []

    def add_value(self, value: float) -> None:
        """Add a value to the buffer if it meets the threshold.

        Args:
            value: The data point to evaluate.

        Raises:
            TypeError: If value is not a float.
        """
        if not isinstance(value, float):
            raise TypeError(f