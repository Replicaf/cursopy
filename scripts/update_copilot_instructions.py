#!/usr/bin/env python3
"""
Auto-generate .github/copilot-instructions.md based on repo structure.

Replaces the AUTOGEN section between markers:
  <!-- AUTOGEN-START -->
  ...generated content...
  <!-- AUTOGEN-END -->

If no markers exist, backs up the file and replaces it completely.
Designed to run from git hooks; exits 0 and prints the file path if modified.
"""
from __future__ import annotations
import os
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / ".github" / "copilot-instructions.md"
BACKUP = TARGET.with_suffix('.md.bak')
AUTOGEN_START = '<!-- AUTOGEN-START -->'
AUTOGEN_END = '<!-- AUTOGEN-END -->'


def find_lessons(base: Path) -> list[Path]:
    """Find all Python lesson files in tipos/ directory."""
    lessons = []
    tipos = base / 'tipos'
    if not tipos.exists():
        return lessons
    for root, dirs, files in os.walk(tipos):
        # ignore __pycache__ and hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith('.')
                   and d != '__pycache__']
        for f in files:
            if f.endswith('.py'):
                lessons.append(Path(root) / f)
    lessons.sort()
    return lessons


def summary_from_filename(p: Path) -> str:
    """Extract lesson topic from filename (01-variables.py -> variables)."""
    name = p.name
    # remove prefixes like 'NN-'
    name = re.sub(r'^\d+\s*-\s*', '', name)
    name = name.replace('.py', '')
    name = name.replace('-', ' ')
    return name


def build_autogen_content(base: Path) -> str:
    """Build auto-generated content block for copilot instructions."""
    lessons = find_lessons(base)
    lines = []
    lines.append(AUTOGEN_START)
    lines.append('')
    lines.append(
        f"**Auto-generated**: Actualizado el "
        f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append('')
    lines.append('**Lecciones detectadas (lista generada automáticamente):**')
    lines.append('')
    if not lessons:
        lines.append('- (No se encontraron archivos en `tipos/`)')
    else:
        for p in lessons:
            rel = p.relative_to(base)
            label = summary_from_filename(p)
            lines.append(f"- `{rel}`: {label}")
    lines.append('')
    lines.append(
        '**Recomendación:** Mantén cada lección independiente '
        'y ejecutable con `python <archivo>.py`.')
    lines.append('')
    lines.append('<!-- End of generated list -->')
    lines.append('')
    lines.append(AUTOGEN_END)
    lines.append('')
    return '\n'.join(lines)


def load_existing(path: Path) -> str | None:
    """Load existing file content or return None if not found."""
    if not path.exists():
        return None
    return path.read_text(encoding='utf-8')


def write_target(path: Path, content: str) -> None:
    """Write content to target file, creating parent dirs as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def merge_or_replace(target: Path, autogen_content: str) -> bool:
    """Update or create target file with autogen content.

    Returns True if file was modified, False otherwise.
    """
    existing = load_existing(target)
    if existing is None:
        header = ("# Copilot Instructions - cursopy\n\n"
                  "Este archivo se ha generado automáticamente. "
                  "Revisa antes de commitear.\n\n")
        new = header + autogen_content
        write_target(target, new)
        return True

    if AUTOGEN_START in existing and AUTOGEN_END in existing:
        # replace content between markers
        pattern = re.compile(re.escape(AUTOGEN_START) +
                             r'.*?' + re.escape(AUTOGEN_END), re.S)
        new_text = pattern.sub(autogen_content, existing)
        if new_text != existing:
            # backup
            BACKUP.write_text(existing, encoding='utf-8')
            write_target(target, new_text)
            return True
        return False
    else:
        # No markers: backup and replace whole file
        BACKUP.write_text(existing, encoding='utf-8')
        header = ("# Copilot Instructions - cursopy\n\n"
                  "(Este archivo fue reemplazado automáticamente; "
                  "el original se guarda como .bak)\n\n")
        new = header + autogen_content
        write_target(target, new)
        return True


if __name__ == '__main__':
    GENERATED_CONTENT = build_autogen_content(ROOT)
    IS_CHANGED = merge_or_replace(TARGET, GENERATED_CONTENT)
    if IS_CHANGED:
        print(f"Updated: {TARGET}")
    else:
        print("No changes needed")
    # exit 0 always; hook will `git add` if the file changed
    raise SystemExit(0)
