# SkillForge 🛠️

**A repository-aware AI developer tool that helps contributors understand codebases, generate project-specific agent skills, and diagnose development errors.**

SkillForge is an open-source, Python-based CLI designed to reduce the friction of working with unfamiliar repositories. It combines deterministic repository inspection with AI-powered generation to help developers understand project structure and create reusable development workflows.

## The Problem

Joining an unfamiliar codebase can be difficult. Developers often need to figure out:

- Where the application starts and which files matter.
- How the project is structured and tested.
- Which conventions AI coding agents should follow.
- What a confusing terminal error means.
- How to establish a basic CI workflow.

Generic AI assistants can explain code, but they may not have reliable, structured knowledge of a particular repository.

## The Solution

SkillForge brings these workflows into one CLI. It inspects repository metadata, uses AI to generate useful artifacts, and provides terminal-based diagnostics.

### Features

- **Codebase Onboarding** — Generates `NEWBIE_GUIDE.md` with repository structure, candidate entry points, and setup guidance.
- **Agent Skill Generation** — Generates project-specific `SKILL.md` instructions for AI coding agents.
- **Log Triage** — Classifies common terminal errors using a local model.
- **CI Workflow Generation** — Generates a GitHub Actions workflow based on detected project metadata.
- **Merge Conflict Assistance** — Uses file content and recent Git history to propose a merged version for review.
- **Repository Tree** — Displays a readable directory tree in the terminal.
- **Command Runner** — Executes selected commands and attempts to classify failures.
- **Atomic File Writes** — Uses temporary files and atomic replacement when writing generated artifacts.

## AI Architecture

SkillForge separates local error classification from hosted text generation.

| Component | Technology | Purpose |
|---|---|---|
| Local inference | Laya inference library | Classify error logs locally |
| Hosted generation | Qwen model through Groq | Generate guides, skills, CI workflows, and conflict-resolution proposals |
| Repository inspection | Python | Detect candidate entry points, test runners, and files |
| CLI interface | argparse + Rich | Commands and terminal output |
| File management | Python filesystem APIs | Write generated artifacts |

**Open-weight AI:** SkillForge incorporates model-based inference rather than training a model from scratch. The local and hosted components have different execution and privacy characteristics.

> **Current implementation note:** The submitted version configures Qwen through Groq for text generation. An Ollama-based Qwen provider is not yet implemented in this version. Verify the exact model identifiers and licenses before making model-specific claims.

## Requirements

- Python 3.13 or newer
- [`uv`](https://docs.astral.sh/uv/)
- Git for repository-related operations
- A Groq API key for hosted text generation
- A working local environment for the Laya inference dependency

## Installation

Clone the repository:

```bash
git clone https://github.com/vicky-404/skillforge.git
cd skillforge
```

Install dependencies:

```bash
uv sync
```

Configure environment variables:

```bash
cp .env.example .env
```

Add your API key to `.env`:

```dotenv
GROQ_API_KEY=your_api_key_here
```

Keep `.env` private. Never commit API keys or other credentials.

## Usage

Run commands from the repository root.

### 1. Explore the repository

```bash
uv run python main.py tree
```

### 2. Generate a newcomer guide

```bash
uv run python main.py onboard
```

Output:

```text
NEWBIE_GUIDE.md
```

### 3. Generate agent skills

```bash
uv run python main.py skills
```

Output:

```text
.agents/skills/python-conventions/SKILL.md
```

### 4. Generate a GitHub Actions workflow

```bash
uv run python main.py ci
```

Output:

```text
.github/workflows/ci.yml
```

Review generated files before using them in a real project.

### 5. Diagnose an existing log file

```bash
uv run python main.py debug test_error.log
```

The local classifier returns an error category and confidence score. This is triage, not a guaranteed root-cause diagnosis.

### 6. Run a command and inspect failures

```bash
uv run python main.py run -- pytest -q
```

SkillForge executes the selected command and attempts to classify the error if it fails.

### 7. Assist with a merge conflict

```bash
uv run python main.py resolve path/to/conflicted_file.py
```

Inspect the proposed resolution carefully. Do not accept generated code without reviewing and testing it.

## Project Structure

```text
skillforge/
├── main.py
├── core/
│   ├── provider.py
│   ├── miners.py
│   └── atomicFS.py
├── prompts/
│   ├── onboard.md
│   ├── skills.md
│   ├── ci.md
│   └── resolve.md
├── test/
├── NEWBIE_GUIDE.md
├── pyproject.toml
├── uv.lock
├── .env.example
└── README.md
```

## Development and Testing

Run the test suite:

```bash
uv run pytest
```

Run an individual test file:

```bash
uv run pytest test/test_core.py -v
```

Test discovery depends on the configured pytest paths and the actual location of your test files.

## Safety and Limitations

- Generated documentation and skills can contain incorrect assumptions. Verify important claims against the source code.
- Log classification identifies likely categories; it does not guarantee a correct root cause.
- Generated CI workflows must be reviewed and validated before being used.
- Merge-conflict proposals may omit important behavior. Inspect the diff and run relevant tests.
- The command runner executes the commands you provide. Only run commands you trust.
- Do not send secrets, credentials, or private source code to hosted AI providers unless you understand and accept the privacy implications.

## Roadmap

- Add an Ollama-based Qwen provider for local text generation.
- Improve repository analysis with source-level relationships and evidence references.
- Validate generated agent skills before writing them.
- Add preview and diff workflows for generated files.
- Generate targeted tests for selected functions and verify their results.
- Improve root-cause analysis by combining logs, source code, and test output.
- Add optional Graphify integration for repository graph updates.
- Add opt-in command history with privacy controls.

## Contributing

Contributions, issues, and suggestions are welcome. Start by opening an issue describing the problem or proposed improvement, then submit a pull request with a clear explanation and relevant tests.

## License

SkillForge is intended to be released under the MIT License.

---

**SkillForge — understand the codebase, teach the agent, improve the workflow.**
