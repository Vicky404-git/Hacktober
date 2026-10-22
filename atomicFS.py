import os
import tempfile
from pathlib import Path

def write_markdown_atomic(target_path: str, content: str) -> None:
    """Atomic write to prevent file corruption during skill generation."""
    path = Path(target_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    fd, temp_path = tempfile.mkstemp(dir=path.parent, prefix=".tmp_")
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, path)
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise e
