import sys
import argparse
from atomicFS import write_markdown_atomic
from provider import (
    classify_log_fast, 
    generate_skill_content, 
    resolve_conflict_with_context
)

def main():
    parser = argparse.ArgumentParser(description="SkillForge Dev Copilot")
    subparsers = parser.add_subparsers(dest="command")

    # Command: onboard
    subparsers.add_parser("onboard", help="Generate NEWBIE_GUIDE.md")

    # Command: skills
    subparsers.add_parser("skills", help="Generate project SKILL.md rules")

    # Command: debug
    debug_parser = subparsers.add_parser("debug", help="Triage failing terminal log")
    debug_parser.add_argument("log_file", help="Path to log or stderr file")

    # Command: resolve
    resolve_parser = subparsers.add_parser("resolve", help="Context-Aware Merge Conflict Copilot")
    resolve_parser.add_argument("file_path", help="Path to file with git merge conflicts")

    args = parser.parse_args()

    if args.command == "onboard":
        print("🔍 Scanning project files...")
        guide_prompt = "Generate a short NEWBIE_GUIDE.md explaining entry points and setup for a Python project."
        content = generate_skill_content(guide_prompt)
        write_markdown_atomic("NEWBIE_GUIDE.md", content)
        print("✅ NEWBIE_GUIDE.md generated successfully!")

    elif args.command == "skills":
        print("🧠 Analyzing architectural conventions...")
        prompt = """Generate a valid agentskills.io SKILL.md file with frontmatter:
---
name: python-code-conventions
description: Coding standards and error handling rules for this repo.
---
# Python Standards
1. Use type hints for all public functions.
2. Handle exceptions explicitly with custom error classes.
"""
        content = generate_skill_content(prompt)
        write_markdown_atomic(".agents/skills/python-conventions/SKILL.md", content)
        print("✅ Created .agents/skills/python-conventions/SKILL.md!")

    elif args.command == "debug":
        with open(args.log_file, "r", encoding="utf-8") as f:
            log_data = f.read()
        res = classify_log_fast(log_data)
        print(f"⚡ Jev/Laya Triage Output (Fast Classification): {res}")

    elif args.command == "resolve":
        print(f"🔀 Analyzing Git merge conflict in {args.file_path}...")
        explanation, clean_code = resolve_conflict_with_context(args.file_path)
        
        print("\n💡 Conflict Breakdown:")
        print(explanation)
        
        # Atomically write resolved content back to disk
        write_markdown_atomic(args.file_path, clean_code)
        print(f"\n✅ Automatically resolved and wrote clean code to {args.file_path}!")

if __name__ == "__main__":
    main()
