import os
from pathlib import Path

IGNORE_DIRS = {".git", ".venv", "__pycache__", "node_modules", "target", ".agents", "dist", "build"}

def scan_repository(root_path: str = ".") -> dict:
    """Scans repo structure, entry points, and test runners deterministically."""
    root = Path(root_path)
    
    # Identify entry points
    entry_candidates = ["main.py", "app.py", "index.js", "Cargo.toml", "go.mod", "pyproject.toml", "setup.py"]
    found_entry_points = [item for item in entry_candidates if (root / item).exists()]
    
    # Identify test runner candidates
    test_runners = []
    if (root / "tests").exists() or list(root.glob("**/test_*.py")):
        test_runners.append("pytest")
    if (root / "package.json").exists():
        test_runners.append("npm test")
    if (root / "Cargo.toml").exists():
        test_runners.append("cargo test")

    # Sample file tree (top 25 files)
    file_tree = []
    for p in root.rglob("*"):
        if any(part in IGNORE_DIRS for part in p.parts):
            continue
        if p.is_file():
            file_tree.append(str(p.relative_to(root)))
        if len(file_tree) >= 25:
            break

    return {
        "entry_points": found_entry_points,
        "test_runners": test_runners,
        "tree_sample": "\n".join(file_tree)
    }
