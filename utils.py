"""
utils.py – Shared helpers.
"""

import subprocess
from pathlib import Path


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def init_git_repo(target_dir: Path) -> None:
    try:
        subprocess.run(["git", "init"], cwd=target_dir, capture_output=True, check=True)
    except Exception as e:
        print(f"  ⚠️  Git init skipped: {e}")
