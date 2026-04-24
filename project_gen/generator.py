"""
generator.py – Writes the generated project to disk.
Works for both CLI and web server modes.
"""

import os
import shutil
import zipfile
import tempfile
from pathlib import Path
from typing import Dict, Tuple

from project_gen.stacks import build_files, resolve_stack, STACK_META


def _write_files(files: Dict[str, str], target_dir: Path) -> None:
    """Write all file contents to the target directory."""
    for rel_path, content in files.items():
        output = target_dir / rel_path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")


def _init_git(target_dir: Path) -> None:
    """Initialise a git repo and write a .gitignore."""
    import subprocess
    gitignore_content = (
        "# Dependencies\nnode_modules/\nvenv/\n.venv/\n\n"
        "# Environment\n.env\n*.env.local\n\n"
        "# Build outputs\ndist/\nbuild/\n.next/\nout/\nstaticfiles/\n\n"
        "# Python\n__pycache__/\n*.pyc\n*.pyo\n*.pyd\n.Python\n*.egg-info/\n\n"
        "# Misc\n.DS_Store\n*.log\ncoverage/\n.coverage\n"
    )
    (target_dir / ".gitignore").write_text(gitignore_content, encoding="utf-8")
    try:
        subprocess.run(["git", "init"], cwd=target_dir, capture_output=True, check=True)
        subprocess.run(
            ["git", "add", ".gitignore"],
            cwd=target_dir, capture_output=True
        )
    except Exception as e:
        print(f"  ⚠️  Git init skipped: {e}")


# ─────────────────────────────────────────────
# CLI mode – write to a named folder on disk
# ─────────────────────────────────────────────

def generate_project_to_disk(options: dict, project_name: str) -> Path:
    """
    Generate the full project into ./<project_name>/.
    Returns the Path of the created directory.
    """
    stack_id = resolve_stack(options["platform"], options["category"])
    ctx = {**options, "project_name": project_name}

    target_dir = Path.cwd() / project_name
    target_dir.mkdir(exist_ok=True)

    files = build_files(stack_id, ctx)
    _write_files(files, target_dir)
    _init_git(target_dir)

    meta = STACK_META.get(stack_id, {})
    return target_dir, stack_id, meta


# ─────────────────────────────────────────────
# Web / API mode – return an in-memory ZIP
# ─────────────────────────────────────────────

def generate_project_to_zip(options: dict, project_name: str) -> Tuple[bytes, str, dict]:
    """
    Generate the full project into a ZIP archive in memory.
    Returns (zip_bytes, stack_id, stack_meta).
    """
    stack_id = resolve_stack(options["platform"], options["category"])
    ctx = {**options, "project_name": project_name}
    files = build_files(stack_id, ctx)

    # Build .gitignore
    gitignore = (
        "node_modules/\nvenv/\n.venv/\n.env\ndist/\nbuild/\n.next/\n"
        "__pycache__/\n*.pyc\n.DS_Store\ncoverage/\nstaticfiles/\n"
    )
    files[".gitignore"] = gitignore

    # Pack into ZIP (all files under project_name/)
    import io
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel_path, content in files.items():
            zf.writestr(f"{project_name}/{rel_path}", content)
    buf.seek(0)

    meta = STACK_META.get(stack_id, {})
    return buf.read(), stack_id, meta
