# NEWBIE_GUIDE.md

Welcome to the team! This guide will help you navigate the repository, understand its structure, and get your local environment up and running quickly.

## 1. Where to Start Reading Code

Based on the detected entry points, here is the recommended reading order to understand the application's core logic:

1.  **`main.py`**: This is the primary entry point of the application. Start here to understand the initial execution flow, how the app initializes, and which modules are imported and invoked at startup.
2.  **`pyproject.toml`**: Review this file to understand the project's dependencies, Python version requirements, and configuration for tools like `uv` (package manager) and `pytest` (testing framework).
3.  **Core Modules**:
    *   **`provider.py`**: Likely contains the core logic for providing services or data.
    *   **`miners.py`**: Suggests data mining or processing logic.
    *   **`atomicFS.py`**: Appears to be a custom file system utility, possibly for atomic operations.
    *   **`conflicted_app.py`**: This name suggests it might be a legacy, experimental, or conflicting version of an app module. Investigate its relationship with `main.py` and `provider.py`.

> **Tip**: Use the `graphify-out/` directory (specifically `GRAPH_REPORT.md` and `graph.html`) if available in your environment. These files likely contain generated dependency graphs that can help visualize relationships between modules.

## 2. Running and Testing Locally

### Prerequisites
- **Python**: Check the required version in `pyproject.toml` or `.python-version`.
- **uv**: The presence of `uv.lock` indicates this project uses [uv](https://docs.astral.sh/uv/) for fast Python package management. Install it if you haven't already:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### Setup
1.  **Clone the repository**.
2.  **Install Dependencies**:
    ```bash
    uv sync
    ```
    This will create a virtual environment and install all dependencies listed in `pyproject.toml` using the lock file.
3.  **Configure Environment Variables**:
    - Copy `.env.example` to `.env`:
      ```bash
      cp .env.example .env
      ```
    - Edit `.env` with the necessary credentials or configuration values. **Never commit `.env` to version control.**

### Running the Application
Assuming `main.py` is the entry point:
```bash
uv run python main.py
```
Or, if defined in `pyproject.toml`, there might be a script entry point:
```bash
uv run <script-name>
```
Check `pyproject.toml` under `[project.scripts]` for specific commands.

### Running Tests
The project uses `pytest`. To run all tests:
```bash
uv run pytest
```
To run a specific test file (e.g., if tests are in a `tests/` directory, though not explicitly listed in the sample, they might be co-located or in a hidden folder):
```bash
uv run pytest path/to/test_file.py
```
Check `pyproject.toml` for specific `pytest` configuration (e.g., test paths, markers).

## 3. Architecture Layout Overview

Based on the file tree, here is a high-level overview of the repository structure:

- **Core Application Logic**:
  - `main.py`: Entry point and orchestration.
  - `provider.py`: Core service/provider logic.
  - `miners.py`: Data processing/mining components.
  - `conflicted_app.py`: Potentially an alternate or legacy app module.

- **Utilities & Infrastructure**:
  - `atomicFS.py`: Custom file system utilities.
  - `.env` / `.env.example`: Environment configuration.

- **Project Configuration**:
  - `pyproject.toml`: Project metadata, dependencies, and tool configuration.
  - `uv.lock`: Lock file for reproducible dependency installation.
  - `.python-version`: Specifies the Python version.

- **Documentation & Metadata**:
  - `README.md`: General project documentation.
  - `LICENSE`: Licensing information.
  - `NEWBIE_GUIDE.md`: This file.

- **Generated Artifacts (Do Not Edit)**:
  - `graphify-out/`: Contains generated dependency graphs, analysis JSON, and HTML visualizations. These are likely produced by a tool called `graphify` and should not be manually modified.
  -