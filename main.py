import sys
import argparse
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.tree import Tree
from core.atomicFS import write_markdown_atomic
from core.provider import (
    classify_log_fast, 
    generate_onboard_guide,
    generate_skill_rules,
    generate_ci_workflow,
    resolve_conflict_with_context
)

console = Console()

def render_repo_tree(dir_path: Path, tree_node: Tree, ignore_dirs=None):
    if ignore_dirs is None:
        ignore_dirs = {".git", ".venv", "__pycache__", "node_modules", ".pytest_cache", "graphify-out", ".agents"}
        
    for path in sorted(dir_path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
        if path.name in ignore_dirs or path.name.startswith("."):
            continue
        if path.is_dir():
            branch = tree_node.add(f"[bold blue]📁 {path.name}/[/bold blue]")
            render_repo_tree(path, branch, ignore_dirs)
        else:
            tree_node.add(f"[cyan]📄 {path.name}[/cyan]")

def main():
    parser = argparse.ArgumentParser(description="SkillForge Dev Copilot")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("onboard", help="Generate NEWBIE_GUIDE.md")
    subparsers.add_parser("skills", help="Generate project SKILL.md rules")
    subparsers.add_parser("ci", help="Generate .github/workflows/ci.yml")
    subparsers.add_parser("tree", help="Display visual codebase directory tree")

    debug_parser = subparsers.add_parser("debug", help="Triage failing terminal log file")
    debug_parser.add_argument("log_file", help="Path to log file")

    resolve_parser = subparsers.add_parser("resolve", help="Context-Aware Merge Conflict Copilot")
    resolve_parser.add_argument("file_path", help="Path to conflicted file")

    run_parser = subparsers.add_parser("run", help="Run a command live and catch errors for instant triage")
    run_parser.add_argument("cmd", nargs=argparse.REMAINDER, help="Command to execute")

    args = parser.parse_args()

    if args.command == "tree":
        root = Path(".")
        tree_view = Tree(f"[bold green]📦 {root.resolve().name}[/bold green]")
        render_repo_tree(root, tree_view)
        console.print(Panel(tree_view, title="🌳 SkillForge Project Structure", border_style="green"))


    elif args.command == "onboard":
        with console.status("[bold cyan]Scanning repository & authoring onboarding guide...", spinner="dots"):
            guide = generate_onboard_guide()
            write_markdown_atomic("NEWBIE_GUIDE.md", guide)
        console.print(Panel("[bold green]✅ NEWBIE_GUIDE.md created successfully![/bold green]", title="SkillForge Onboard"))
        console.print("Below is the Guide:\n")
        console.print(guide)

    elif args.command == "skills":
        with console.status("[bold magenta]Analyzing code patterns & generating skill rules...", spinner="dots"):
            rules = generate_skill_rules()
            write_markdown_atomic(".agents/skills/python-conventions/SKILL.md", rules)
        console.print(Panel("[bold green]✅ Created .agents/skills/python-conventions/SKILL.md[/bold green]", title="SkillForge Skills"))

    elif args.command == "ci":
        with console.status("[bold yellow]Generating GitHub Actions CI workflow...", spinner="dots"):
            ci_yaml = generate_ci_workflow()
            write_markdown_atomic(".github/workflows/ci.yml", ci_yaml)
        console.print(Panel("[bold green]✅ Created .github/workflows/ci.yml[/bold green]", title="SkillForge CI"))

    elif args.command == "debug":
        with console.status("[bold red]Triaging log with local System One (Laya)...", spinner="dots"):
            with open(args.log_file, "r", encoding="utf-8") as f:
                log_data = f.read()
            res = classify_log_fast(log_data)
            cause = res['answers']['error_type']['choice']
            conf = res['answers']['error_type']['confidence']
        console.print(Panel(f"[bold yellow]Root Cause Category:[/bold yellow] [cyan]{cause}[/cyan]\n[bold yellow]Confidence Score:[/bold yellow] [green]{conf:.2f}[/green]", title="⚡ Local Laya Triage Result"))
    
    elif args.command == "resolve":
        with console.status("[bold blue]Parsing git log context & resolving merge conflict with Qwen...", spinner="dots"):
            explanation, clean_code = resolve_conflict_with_context(args.file_path)
        
        console.print(Panel(explanation, title="💡 Conflict Breakdown & Resolution Context", border_style="blue"))
        
        # Interactive confirmation prompt for beginner safety
        confirm = console.input("\n[bold yellow]🤖 Do you want SkillForge to apply this fix and stage the file? (y/N): [/bold yellow]").strip().lower()
        
        if confirm in ["y", "yes"]:
            write_markdown_atomic(args.file_path, clean_code)
            subprocess.run(["git", "add", args.file_path])
            console.print(Panel(f"[bold green]✅ Fix applied atomically and staged via `git add {args.file_path}`![/bold green]"))
            
            push_confirm = console.input("[bold yellow]🚀 Would you like to commit and push now? (y/N): [/bold yellow]").strip().lower()
            if push_confirm in ["y", "yes"]:
                commit_msg = console.input("[bold cyan]Enter commit message (default: 'fix: resolve merge conflicts via SkillForge'): [/bold cyan]").strip()
                if not commit_msg:
                    commit_msg = "fix: resolve merge conflicts via SkillForge"
                
                subprocess.run(["git", "commit", "-m", commit_msg])
                res = subprocess.run(["git", "push"], capture_output=True, text=True)
                
                if res.returncode == 0:
                    console.print("[bold green]🎉 Pushed successfully to remote![/bold green]")
                else:
                    console.print(Panel(f"[bold red]❌ Push failed:[/bold red]\n{res.stderr}", title="Git Error"))
            else:
                console.print("[bold dim]Staged. Ready for manual push when you're ready.[/bold dim]")
        else:
            console.print("[bold dim]Operation cancelled. Local file untouched.[/bold dim]")

    elif args.command == "run":
        if not args.cmd:
            console.print("[bold red]⚠️ Specify a command to run (e.g. uv run main.py run -- pytest)[/bold red]")
            sys.exit(1)
            
        cmd = args.cmd[1:] if args.cmd[0] == "--" else args.cmd
        console.print(f"[bold dim]🚀 Executing live command: {' '.join(cmd)}[/bold dim]\n")
        
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            console.print(Panel("[bold red]❌ Command Failed! Intercepting stderr for instant local triage...[/bold red]"))
            res = classify_log_fast(proc.stderr)
            cause = res['answers']['error_type']['choice']
            console.print(Panel(f"[bold yellow]Root Cause:[/bold yellow] [bold cyan]{cause}[/bold cyan]", title="⚡ System 1 (Laya) Fast Triage"))
            syntax = Syntax(proc.stderr[-400:], "pytb", theme="monokai", line_numbers=True)
            console.print(Panel(syntax, title="Terminal Stderr Snippet"))
        else:
            console.print(proc.stdout)
            console.print("[bold green]✅ Command executed cleanly![/bold green]")

if __name__ == "__main__":
    main()
