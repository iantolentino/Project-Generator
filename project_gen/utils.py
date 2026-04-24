import subprocess
from pathlib import Path


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def init_git_repo(target_dir: Path):
    try:
        subprocess.run(["git", "init"], cwd=target_dir, check=True)
    except Exception:
        print("⚠️ Git init skipped")