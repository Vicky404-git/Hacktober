# NEWBIE_GUIDE.md

Welcome to **SkillForge** 🛠️. This guide helps you navigate the codebase, understand the architecture, and get running locally.

## 1. Where to Start Reading Code

Based on the repository metadata and graph analysis, here is the recommended reading order:

1.  **`main.py`**: This is the primary entry point.
    *   It contains the `main()` function, which is a "God Node" (highly connected) in the dependency graph.
    *   It orchestrates the application flow by calling core functions like `generate_onboard_guide()`, `scan_repository()`, and `write_markdown_atomic()`.
    *   *Start here to understand the high-level workflow.*

2.  **`core/provider.py`**: This module contains the core business logic.
    *   Key functions include `generate_onboard_guide()`, `generate_skill_rules()`, `resolve_conflict_with_context()`, and `load_prompt_template()`.
    *   `main.py` relies heavily on this module (see "Surprising Connections" in the graph report).
    *   *Read this to understand how the AI generation and conflict resolution logic works.*

3.  **`core/miners.py`**: Contains `scan_repository()`, another key node called by both `main.py` and tests.
    *   Responsible for analyzing the repository structure.

4.  **`core/atomicFS.py`**: Contains `write_markdown_atomic()`.
    *   This utility ensures safe file writes. It is a bridge between the core logic and the file system, tested directly in `test/test_core.py`.

5.  **`prompts/`**: Contains template files (e.g., `onboard.md`, `ci.md`, `resolve.md`) that are loaded by `load_prompt_template()` in `core/provider.py`.
    *   *Read these to understand the output formats and AI instructions.*

## 2. How to Run and Test the App Locally

### Prerequisites
*   **Python**: Check `.python-version` for the required version.
*   **Environment**: The project uses `uv` for dependency management (indicated by `uv.lock`).

### Setup
1.  Install dependencies using `uv`:
    ```bash
    uv sync
    ```
2.  Configure environment variables:
    ```bash
    cp .env.example .env
    # Edit .env as needed
    ```

### Running the Application
Execute the main entry point:
```bash
uv run python main.py
```

### Running Tests
The project uses **pytest**. Tests are located in the `test/` directory.
```bash
uv run pytest
```

Key test files:
*   `test/test_core.py`: Tests for `write_markdown_atomic()`, `scan_repository()`, and `load_prompt_template()`.

## 3. Architecture Layout Overview

The project follows a modular structure with clear separation between entry points, core logic, and resources.

```
.
├── main.py                 # Entry point: Orchestrates the application flow
├── core/                   # Core business logic
│   ├── __init__.py
│   ├── atomicFS.py         # Atomic file writing utilities
│   ├── miners.py           # Repository scanning logic
│   └── provider.py         # Main logic: Guide generation, conflict resolution, prompt loading
├── prompts/                # Templates for AI outputs
│   ├── ci.md
│   ├── onboard.md
│   ├── resolve.md
│   └── skills.md
├── test/                   # Pytest test suite
│   └── test_core.py
├── pyproject.toml          # Project configuration and dependencies
├── uv.lock                 # Dependency lock file
└── .github/workflows/ci.yml # CI/CD pipeline
```

### Key Relationships (from Graph Report)
*   **`main.py` → `core/provider.py`**: `main()` calls `generate_onboard_guide()` and other provider functions.
*   **`main.py` → `core/atomicFS.py`**: `main()` uses `write_markdown_atomic()` to safely write outputs.
*   **`core/provider.py` → `prompts/`**: `load_prompt_template()` reads from the `prompts/` directory.
*   **Tests**: `test/test_core.py` directly tests functions from `core/atomicFS.py`, `core/miners.py`, and `core/provider.py`.

### Notable Features
*   **Atomic Writes**: The use of `write_markdown_atomic()` suggests a focus on robust file operations.
*  