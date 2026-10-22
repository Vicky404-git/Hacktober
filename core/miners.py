import json
import shutil
import subprocess
from pathlib import Path

IGNORE_DIRS = {
    ".git", ".venv", "venv", "__pycache__", "node_modules",
    ".pytest_cache", "dist", "build", ".agents", ".mypy_cache",
    ".ruff_cache", "graphify-out",
}

TEXT_SUFFIXES = {
    ".md", ".txt", ".json", ".yaml", ".yml", ".toml",
    ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs",
}


def scan_repository(root_path: str = ".") -> dict:
    """Scan repository metadata deterministically; never requires an LLM."""
    root = Path(root_path).resolve()

    entry_candidates = [
        "main.py", "app.py", "manage.py", "main.js", "index.js",
        "src/main.py", "src/main.js", "pyproject.toml", "package.json",
        "Cargo.toml", "go.mod", "Makefile",
    ]
    entry_points = [
        item for item in entry_candidates if (root / item).is_file()
    ]

    test_runners = []
    if (
        (root / "tests").is_dir()
        or (root / "test").is_dir()
        or any(root.rglob("test_*.py"))
    ):
        test_runners.append("pytest")
    if (root / "package.json").is_file():
        test_runners.append("npm test")
    if (root / "Cargo.toml").is_file():
        test_runners.append("cargo test")
    if (root / "go.mod").is_file():
        test_runners.append("go test ./...")

    files = []
    for path in sorted(root.rglob("*")):
        if any(part in IGNORE_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file():
            files.append(path.relative_to(root).as_posix())
            if len(files) >= 100:
                break

    return {
        "entry_points": entry_points,
        "test_runners": test_runners,
        "tree_sample": "\n".join(files[:40]),
    }


def _run_graphify(args: list[str], root: Path, timeout: int = 30) -> dict:
    """Run Graphify safely without a shell and return captured output."""
    executable = shutil.which("graphify")
    if not executable:
        return {"ok": False, "message": "Graphify is not installed or not on PATH."}

    try:
        proc = subprocess.run(
            [executable, *args],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout[-12000:],
            "stderr": proc.stderr[-3000:],
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "message": f"Graphify timed out after {timeout}s."}
    except OSError as exc:
        return {"ok": False, "message": str(exc)}


def refresh_graphify(root: str = ".") -> dict:
    """Update the project's graph using the installed Graphify CLI."""
    root_path = Path(root).resolve()
    if not (root_path / ".git").exists():
        return {
            "ok": False,
            "message": "Not a Git repository; refusing automatic graph update.",
        }
    result = _run_graphify(["update", str(root_path)], root_path, timeout=120)
    if result.get("ok"):
        result["message"] = "Graphify graph updated successfully."
    else:
        result.setdefault("message", result.get("stderr", "Graphify update failed."))
    return result


def get_graphify_context(root: str = ".") -> dict:
    """Read Graphify reports and graph data for beginner-friendly explanations."""
    root_path = Path(root).resolve()
    output_dir = root_path / "graphify-out"
    result = {
        "available": False,
        "status": "unavailable",
        "summary": "",
        "reports": [],
        "message": "",
    }

    if not shutil.which("graphify"):
        result["message"] = "Graphify CLI not found; using deterministic scanning."
        return result

    if not output_dir.is_dir():
        result["message"] = (
            "No graphify-out directory found. Run `graphify update .` "
            "from the repository root to create the graph."
        )
        return result

    sections = []
    report_names = ("GRAPH_REPORT.md", "graph_report.md", "README.md")

    for name in report_names:
        path = output_dir / name
        if path.is_file():
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
                if content.strip():
                    sections.append(f"## Graph report: {name}\n{content[:10000]}")
                    result["reports"].append(name)
            except OSError:
                pass

    graph_path = output_dir / "graph.json"
    if graph_path.is_file():
        try:
            data = json.loads(graph_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                nodes = data.get("nodes", [])
                edges = data.get("edges", data.get("links", []))
                sections.append(
                    "## Graph structure (JSON summary)\n"
                    f"Node count: {len(nodes) if isinstance(nodes, list) else 'unknown'}\n"
                    f"Edge count: {len(edges) if isinstance(edges, list) else 'unknown'}\n"
                    "Graph file: graphify-out/graph.json"
                )
                result["reports"].append("graph.json")
        except (OSError, json.JSONDecodeError):
            sections.append("Graph JSON exists but could not be parsed.")

    if sections:
        result.update({
            "available": True,
            "status": "report_found",
            "summary": "\n\n".join(sections)[:16000],
            "message": "Graphify output found.",
        })
    else:
        result["message"] = (
            "Graphify is installed but no readable graph report was found. "
            "Run `graphify update .` and inspect its output."
        )

    return result


def explain_graph_node(target: str, root: str = ".") -> dict:
    """Ask Graphify to explain a file, symbol, or node."""
    root_path = Path(root).resolve()
    return _run_graphify(
        ["explain", target, "--graph", str(root_path / "graphify-out" / "graph.json")],
        root_path,
    )


def query_graph(question: str, root: str = ".") -> dict:
    """Query relationships in the existing Graphify graph."""
    root_path = Path(root).resolve()
    return _run_graphify(
        ["query", question, "--graph", str(root_path / "graphify-out" / "graph.json")],
        root_path,
    )

