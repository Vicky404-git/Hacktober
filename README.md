# SkillForge 🛠️

**Understand an unfamiliar codebase. Find where to start. Give AI coding agents project-specific skills. Diagnose development errors — from your terminal.**

SkillForge is a Python CLI developer companion designed to reduce the friction of joining or working in an unfamiliar repository. It combines deterministic repository scanning, optional [Graphify](https://github.com/graphify) code-relationship analysis, and AI-powered generation to turn a repository into something contributors can navigate and work with.

> Built for developers who want more than a generic chatbot answer: repository-aware guidance, inspectable artifacts, and terminal-first workflows.

## The Problem

When a developer opens an unfamiliar project, they have to discover:

- Which files are the best starting points?
- How do modules and functions relate?
- How do they install, run, and test the project?
- What conventions should an AI coding agent follow?
- What does a confusing terminal error mean?
- How can they resolve a merge conflict without blindly accepting a generated fix?

This discovery work is especially frustrating for first-time contributors. Generic AI assistance may explain a file in isolation without understanding how it fits into the repository.

## The Solution

SkillForge brings several developer workflows into one CLI. It scans the repository, optionally incorporates Graphify's structural report, and uses AI where generated explanations or artifacts are useful.

### Features

- **Beginner Tour** — `tour` shows detected entry points, test runners, and available Graphify repository context, then gives newcomers a practical next-step checklist.
- **Codebase Onboarding** — `onboard` generates `NEWBIE_GUIDE.md` with a suggested reading order, setup and testing guidance, and architecture context.
- **Agent Skill Generation** — `skills` generates project-specific `SKILL.md` instructions for AI coding agents.
- **Log Triage** — `debug` uses a local Laya model to classify common terminal errors.
- **CI Workflow Generation** — `ci` generates a GitHub Actions workflow based on detected repository metadata.
- **Merge Conflict Assistance** — `resolve` uses file content and recent Git history to propose a resolution for review.
- **Repository Tree** — `tree` displays a readable directory tree in the terminal.
- **Command Runner** — `run` executes a command and attempts to classify failures.
- **Graphify Integration** — uses an existing Graphify graph/report to surface repository relationships; Graphify remains an optional external CLI.
- **Safer File Writes** — generated artifacts use temporary files and atomic replacement.

## How the Graphify integration works

SkillForge's deterministic scanner identifies candidate entry points, test runners, and a sample of repository files. If Graphify is installed and its output exists, SkillForge can read `graphify-out/GRAPH_REPORT.md` and `graphify-out/graph.json` and include that context in onboarding.

The `tour` command combines the scan with the graph report. The `onboard` command passes the available graph context into the guide-generation prompt. If Graphify is unavailable or no report exists, the tour can fall back to the deterministic scan.

Graphify is an optional dependency: install and run it separately according to its own documentation.

```bash
# From the repository root, after installing Graphify
graphify update .
graphify explain "main.py"
graphify query "Where should a new contributor start?"
graphify path "main()" "write_markdown_atomic()"
graphify affected "core/provider.py"
graphify tree
```

Graph data can become stale after code changes. Refresh it with `graphify update .` before relying on it. Graph relationships are navigation aids, not proof that every relationship is a direct runtime call; verify important claims against source code.

## AI Architecture

SkillForge separates local error classification from hosted text generation.

| Component | Technology | Purpose |
|---|---|---|
| Local inference | Laya inference library | Classifies error logs locally |
| Hosted generation | Qwen through Groq | Generates onboarding guides, agent skills, CI workflows, and conflict-resolution proposals |
| Repository inspection | Python | Detects candidate entry points, test runners, and files |
| Graph context | Graphify CLI (optional) | Supplies code graph and report context |
| CLI interface | `argparse` + Rich | Commands and terminal output |
| File management | Python filesystem APIs | Writes generated artifacts atomically |

**Model note:** this implementation uses a hosted Qwen model through Groq for text generation and a local Laya model for error classification. It does not train a model from scratch, and this version does not implement an Ollama-based Qwen provider. Check the configured model identifier against the provider's current model catalogue.

## Requirements

- Python 3.13 or newer
- [`uv`](https://docs.astral.sh/uv/)
- Git for repository-related operations
- A Groq API key for hosted text generation
- A working environment for the Laya inference dependency
- Graphify CLI only if you want graph-powered context and graph commands

## Installation

Clone the repository:

```bash
git clone https://github.com/Vicky404-git/SkillForge.git
cd SkillForge
```

Install dependencies:

```bash
uv sync
```

Configure environment variables:

```bash
cp .env.example .env
```

Add your Groq API key to `.env`:

```dotenv
GROQ_API_KEY=your_api_key_here
```

Keep `.env` private. Never commit API keys, credentials, or other secrets.

### Optional: Graphify

Install Graphify using its official installation instructions, then build the graph from the repository root:

```bash
graphify update .
```

This creates or refreshes the graph outputs under `graphify-out/`. SkillForge can use the available report for onboarding and its beginner tour.

## Usage

Run commands from the repository root.

### 1. Take the beginner tour

```bash
uv run python main.py tour
```

Shows likely entry points, detected test runners, Graphify context when available, and suggested next steps for a newcomer.

### 2. Explore the repository tree

```bash
uv run python main.py tree
```

### 3. Generate a newcomer guide

```bash
uv run python main.py onboard
```

Output: `NEWBIE_GUIDE.md`

### 4. Generate agent skills

```bash
uv run python main.py skills
```

Output: `.agents/skills/python-conventions/SKILL.md`

### 5. Generate a GitHub Actions workflow

```bash
uv run python main.py ci
```

Output: `.github/workflows/ci.yml`

Review generated files before using them in a real project.

### 6. Diagnose an existing log file

```bash
uv run python main.py debug test_error.log
```

The local classifier returns an error category and confidence score. This is triage, not a guaranteed root-cause diagnosis.

### 7. Run a command and inspect failures

```bash
uv run python main.py run -- pytest -q
```

SkillForge executes the selected command and attempts to classify the error if it fails. Only run commands you trust.

### 8. Assist with a merge conflict

```bash
uv run python main.py resolve path/to/conflicted_file.py
```

SkillForge explains the conflict and proposes merged code. It asks before applying the result and staging the file. Inspect the diff and run relevant tests before committing.

## Project Structure

```text
SkillForge/
├── main.py
├── core/
│   ├── provider.py       # AI generation and error triage
│   ├── miners.py         # Repository scan and Graphify context
│   └── atomicFS.py       # Atomic file writes
├── prompts/
│   ├── onboard.md
│   ├── skills.md
│   ├── ci.md
│   └── resolve.md
├── test/
│   └── test_core.py
├── .github/workflows/
├── .env.example
├── pyproject.toml
├── uv.lock
└── README.md
```

## Development and Testing

Run the test suite:

```bash
uv run pytest
```

Run tests with verbose output:

```bash
uv run pytest test/test_core.py -v
```

Check Python syntax/import compilation:

```bash
uv run python -m compileall main.py core
```

## Safety and Limitations

- AI-generated documentation and skills may contain incorrect assumptions. Verify important claims against source code.
- Graph relationships are useful for navigation but should not be treated as proof of direct runtime behavior without checking the code.
- Log classification identifies likely error categories; it does not guarantee a correct root cause.
- Generated CI workflows must be reviewed and validated.
- Merge-conflict proposals may omit important behavior. Inspect the diff and run relevant tests.
- The command runner executes commands you provide. Only run commands you trust.
- Hosted generation sends the prompt context to the configured provider. Do not submit secrets or private code unless you understand and accept the provider's data-handling terms.
- Graphify is optional. Without a readable graph report, SkillForge falls back to deterministic repository metadata where supported.

## Roadmap

- Improve evidence-linked explanations and source navigation.
- Add previews and diffs before writing generated artifacts.
- Generate targeted tests for selected functions and run them.
- Improve root-cause analysis by combining logs, source code, and test output.
- Add an optional local Qwen/Ollama text-generation provider.
- Expand repository-aware guidance for additional languages and build systems.

## Contributing

Issues, suggestions, and pull requests are welcome. Describe the problem or proposed change, include reproduction steps where possible, and run the test suite before submitting a pull request.

## License

The repository's license should be confirmed from the `LICENSE` file before redistribution.

---

**SkillForge — understand the codebase, guide the contributor, improve the workflow.**
