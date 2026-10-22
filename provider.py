import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from laya import Router

# Force Python to read the .env file in the current directory
load_dotenv()

# Initialize System One (Laya - Local 421M Decision Model)
laya_router = Router(preload=True)

# Initialize System Two (Groq - Qwen2.5-Coder)
llm = ChatGroq(
    model_name="qwen/qwen3.8-27b",
    groq_api_key=os.getenv("GROQ_API_KEY") # This will now successfully pull from .env
)

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
    tail = stderr_text[-1200:]  # the real error is at the bottom of a traceback
    return laya_router.predict({"body": tail}, questions)

def generate_skill_content(prompt: str) -> str:
    """Uses Groq for full markdown generation."""
    response = llm.invoke(prompt)
    return response.content
