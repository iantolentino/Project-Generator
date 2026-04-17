import subprocess
from pathlib import Path

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def init_git_repo(target_dir: Path):
    try:
        subprocess.run(["git", "init"], cwd=target_dir, capture_output=True, check=True)
        gitignore = target_dir / ".gitignore"
        gitignore.write_text("__pycache__/\n*.pyc\n.env\nnode_modules/\n", encoding="utf-8")
    except Exception as e:
        print(f"⚠️  Git initialization skipped: {e}")