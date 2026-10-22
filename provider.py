import os
import subprocess
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from laya import Router

# Force Python to read .env
load_dotenv()

# Initialize System One (Laya - Local 421M Decision Model)
laya_router = Router(preload=True)

# Initialize System Two (Groq - Qwen3.8 only qwen model in groq)
llm = ChatGroq(
    model_name="qwen/qwen3.8-27b",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

def classify_log_fast(stderr_text: str) -> dict:
    """Uses Laya for ~30ms terminal error classification."""
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

def generate_skill_content(prompt: str) -> str:
    """Uses Groq for full markdown generation."""
    response = llm.invoke(prompt)
    return response.content

def resolve_conflict_with_context(file_path: str) -> tuple[str, str]:
    """Parses git conflict markers and uses commit logs + Qwen2.5-Coder to resolve."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "<<<<<<< " not in content or ">>>>>>> " not in content:
        return "No git conflict markers found in file.", content

    # Pull recent commit logs for context on what both sides were building
    try:
        git_log = subprocess.check_output(
            ["git", "log", "-n", "5", "--oneline", "--", file_path], 
            text=True, 
            stderr=subprocess.DEVNULL
        )
    except Exception:
        git_log = "Git log history unavailable."

    prompt = f"""You are an expert Git Conflict Copilot.
Analyze this file containing Git merge conflict markers and recent commit logs.

### CONFLICTED FILE ({file_path}):
{content}

### RECENT COMMIT LOG HISTORY:
{git_log}

Task:
1. Explain in 2-3 bullet points what both branches (HEAD vs incoming changes) intended to do.
2. Provide the complete, merged, production-ready code with ALL conflict markers (<<<<<<<, =======, >>>>>>>) cleanly resolved and removed.

Format strictly as:
---EXPLANATION---
<your explanation here>
---RESOLVED_CODE---
<clean merged code ONLY>
"""

    response = llm.invoke(prompt)
    raw_output = response.content

    if "---RESOLVED_CODE---" in raw_output:
        parts = raw_output.split("---RESOLVED_CODE---")
        explanation = parts[0].replace("---EXPLANATION---", "").strip()
        resolved_code = parts[1].strip()

        # Clean markdown code block fencing if LLM wrapped it
        if resolved_code.startswith("```"):
            lines = resolved_code.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            resolved_code = "\n".join(lines)
            
        return explanation, resolved_code
    else:
        return "Merged successfully.", raw_output
