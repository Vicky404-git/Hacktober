import os
import shutil
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from laya import Router
from core.miners import scan_repository

load_dotenv()

PROMPTS_DIR = Path("prompts")

# System One: Local 421M Laya Model
laya_router = Router(preload=True)

# System Two: Groq Qwen Model
llm = ChatGroq(
    model_name="qwen/qwen3.8-27b",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    max_tokens=1000
)

def load_prompt_template(prompt_name: str) -> str:
    """Loads a prompt template from prompts/<prompt_name>.md."""
    file_path = PROMPTS_DIR / f"{prompt_name}.md"
    if not file_path.exists():
        raise FileNotFoundError(f"Prompt template missing: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def trigger_graphify_hook() -> None:
    """Asynchronously triggers graphify update in background if binary exists."""
    if shutil.which("graphify"):
        try:
            subprocess.Popen(["graphify", "update", "."], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

def classify_log_fast(stderr_text: str) -> dict:
    questions = {
        "error_type": {
            "type": "choice",
            "instructions": "What is the primary cause of this error?",
            "criteria": {
                "syntax_error": "code can't be parsed: SyntaxError, IndentationError",
                "missing_dependency": "module/package/command not found: ModuleNotFoundError, ImportError",
                "test_failure": "an assertion or test case failed",
                "permission_denied": "access refused: PermissionError, EACCES",
                "other": "none of the above",
            },
        }
    }
    tail = stderr_text[-1200:]
    return laya_router.predict({"body": tail}, questions)

def generate_onboard_guide() -> str:
    repo_meta = scan_repository()
    template = load_prompt_template("onboard")
    prompt = template.format(
        entry_points=repo_meta['entry_points'],
        test_runners=repo_meta['test_runners'],
        tree_sample=repo_meta['tree_sample']
    )
    response = llm.invoke(prompt)
    trigger_graphify_hook()
    return response.content

def generate_skill_rules() -> str:
    repo_meta = scan_repository()
    template = load_prompt_template("skills")
    prompt = template.format(entry_points=repo_meta['entry_points'])
    response = llm.invoke(prompt)
    trigger_graphify_hook()
    return response.content

def generate_ci_workflow() -> str:
    repo_meta = scan_repository()
    template = load_prompt_template("ci")
    prompt = template.format(
        entry_points=repo_meta['entry_points'],
        test_runners=repo_meta['test_runners']
    )
    response = llm.invoke(prompt)
    content = response.content
    if "```yaml" in content:
        content = content.split("```yaml")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    return content

def resolve_conflict_with_context(file_path: str) -> tuple[str, str]:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "<<<<<<< " not in content or ">>>>>>> " not in content:
        return "No git conflict markers found in file.", content

    try:
        git_log = subprocess.check_output(
            ["git", "log", "-n", "5", "--oneline", "--", file_path], 
            text=True, 
            stderr=subprocess.DEVNULL
        )
    except Exception:
        git_log = "Git log history unavailable."

    template = load_prompt_template("resolve")
    prompt = template.format(
        file_path=file_path,
        content=content,
        git_log=git_log
    )
    
    response = llm.invoke(prompt)
    raw = response.content

    if "---RESOLVED_CODE---" in raw:
        parts = raw.split("---RESOLVED_CODE---")
        explanation = parts[0].replace("---EXPLANATION---", "").strip()
        resolved_code = parts[1].strip()
        if resolved_code.startswith("```"):
            lines = resolved_code.splitlines()[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            resolved_code = "\n".join(lines)
        trigger_graphify_hook()
        return explanation, resolved_code
    return "Merged successfully.", raw
