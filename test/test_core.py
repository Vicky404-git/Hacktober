import pytest
from pathlib import Path
from core.atomicFS import write_markdown_atomic
from core.miners import scan_repository
from core.provider import load_prompt_template

def test_atomic_write(tmp_path):
    target = tmp_path / "test_output.md"
    content = "# Test Content"
    write_markdown_atomic(str(target), content)
    assert target.exists()
    assert target.read_text(encoding="utf-8") == content

def test_miners_scan():
    repo_meta = scan_repository(".")
    assert "entry_points" in repo_meta
    assert "test_runners" in repo_meta
    assert "tree_sample" in repo_meta

def test_prompt_template_loader():
    prompt_names = ["onboard", "skills", "ci", "resolve"]
    for name in prompt_names:
        template = load_prompt_template(name)
        assert len(template) > 0
