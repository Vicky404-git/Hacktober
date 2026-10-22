# NEWBIE_GUIDE.md

Welcome to the team! This guide will help you get up to speed with the repository structure, how to run the application, and where to focus your attention when reading the code.

## 1. Where to Start Reading Code

Based on the detected entry points, here is the recommended path to understand the core logic:

1.  **`main.py`**: This is the primary entry point. Start here to understand the application's lifecycle, how it initializes, and how it interacts with other modules. Look for the `if __name__ == "__main__":` block to see how the app is launched.
2.  **`pyproject.toml`**: Review this file to understand the project's dependencies, build system configuration, and any custom metadata. This will give you context on what libraries the project relies on.
3.  **Core Modules**: As you read `main.py`, you will likely see imports for the following key modules. Dive into them as needed to understand specific functionalities:
    *   `atomicFS.py`: Likely handles file system operations, possibly with atomic writes for data integrity.
    *   `miners.py`: Suggests logic related to mining or data extraction processes.
    *   `provider.py`: Probably an abstraction layer for data sources or external service providers.
    *   `conflicted_app.py`: May contain logic for handling conflicts or alternative application modes.

**Tip**: Use the `graphify-out/GRAPH_REPORT.md` and `graph.html` files if they are generated in your local environment. These provide visual and textual overviews of the code graph, showing dependencies between modules, which can be very helpful for navigating complex codebases.

## 2. How to Run and Test the App Locally

### Prerequisites
*   **Python**: Check the `.python-version` file to ensure you have the correct Python version installed.
*   **uv**: The presence of `uv.lock` indicates this project uses `uv` for dependency management. Install `uv` if you haven't already.
*   **Environment Variables**: Copy `.env.example` to `.env` and fill in any required environment variables. Check `.env.example` for a list of needed configuration.

### Running the Application
1.  **Install Dependencies**:
    ```bash
    uv sync
    ```
    This command installs all dependencies defined in `pyproject.toml` and `uv.lock`.

2.  **Run the Main Entry Point**:
    ```bash
    uv run python main.py
    ```
    Alternatively, if `pyproject.toml` defines a script entry point, you might be able to run it directly (e.g., `uv run <script-name>`). Check `pyproject.toml` for `[project.scripts]` or similar configuration.

### Testing the Application
The project uses **pytest** for testing.

1.  **Run All Tests**:
    ```bash
    uv run pytest
    ```
2.  **Run Specific Test Files or Functions**:
    ```bash
    uv run pytest path/to/test_file.py
    uv run pytest path/to/test_file.py::test_function_name
    ```
3.  **View Detailed Output**:
    Add `-v` for verbose output:
    ```bash
    uv run pytest -v
    ```

**Note**: Ensure any necessary test fixtures or environment variables are set up as indicated in the test files or `.env.example`.

## 3. Architecture Layout Overview

Here is a high-level overview of the repository structure based on the provided file tree:

*   **Core Application Logic**:
    *   `main.py`: Entry point and main orchestration.
    *   `atomicFS.py`: File system utilities, likely focusing on safe/atomic file operations.
    *   `miners.py`: Core business logic for mining/extraction tasks.
    *   `provider.py`: Abstraction for data/service providers.
    *   `conflicted_app.py`: Possibly handles conflict resolution or alternative application flows.

*   **Configuration & Metadata**:
    *   `pyproject.toml`: Project configuration, dependencies, build system.
    *   `.python-version`: Specifies the required Python version.
    *   `.env` / `.env.example`: Environment variables (keep `.env` out of VCS, use `.env.example` as a template).
    *   `LICENSE`: Licensing information.
    *   `.gitignore`: Files/directories ignored by Git.
    *   `uv.lock`: Lock file for `uv` dependency management.

*   **Documentation**:
    *   `README.md`: General project overview and quick start (start here if you haven't already).
    *   `NEWBIE_GUIDE.md`: This file.
    *   `prompts/skills.md`: May contain prompts or skill definitions related to the project.

*   **Testing**:
    *   `test_error.log`: Log file, possibly from test runs or error tracking (check if it's auto-generated or needs manual review).
    *   Test files (not explicitly listed in the sample, but implied by `pytest` usage) are likely in a `tests/` directory or alongside source files (e.g., `test_main.py`, `test_miners.py`).

*   **Generated Artifacts (Graphify)**:
    *   `graphify-out/`: Contains generated code graph analysis files.
        *   `GRAPH_REPORT.md`: Human-readable report on code structure and dependencies.
        *   `graph.html`: Interactive visualization of the code graph.
        *   `graph.json`, `manifest.json`, `.graphify_*` files: Machine-readable data for the graph generation tool.
    *   *Note: These files are generated and should not be manually edited. They can be very useful for understanding complex dependencies.*

**Key Takeaway**: Focus on `main.py` to understand the flow, then drill down into `miners.py`, `provider.py`, and `atomicFS.py` as you encounter their usage. Use the `graphify-out/` reports for a broader architectural view if the codebase grows complex.