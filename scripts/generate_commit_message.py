#!/usr/bin/env python3
"""Generate a short commit message based on staged changes.

This script writes a generated message into the commit message file passed
as the first argument. It will NOT overwrite an existing non-empty message.

Heuristics:
- If only new files are staged -> `feat(scope): Add ...`
- If only modifications are staged -> `fix(scope): Modify ...` (if .py present)
- Otherwise -> `chore(scope): Update ...`

Designed to be called from `.git/hooks/prepare-commit-msg`.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path


def git_output(args: list[str]) -> str:
    """Execute git command and return output as string."""
    return subprocess.check_output(
        ['git'] + args, stderr=subprocess.DEVNULL).decode('utf-8')


def staged_name_status() -> list[str]:
    """Get list of staged file changes with status (A, M, D)."""
    out = git_output(['diff', '--cached', '--name-status'])
    return [l for l in out.splitlines() if l.strip()]


def categorize(lines: list[str]):
    """Categorize git status lines into adds, modifies, deletes."""
    adds, mods, dels = [], [], []
    for l in lines:
        parts = l.split('\t')
        if len(parts) < 2:
            continue
        status = parts[0].strip()
        path = parts[-1].strip()
        if status == 'A':
            adds.append(path)
        elif status == 'M':
            mods.append(path)
        elif status == 'D':
            dels.append(path)
        else:
            mods.append(path)
    return adds, mods, dels


def determine_scope(paths: list[str]) -> str | None:
    """Determine commit scope from changed file paths."""
    if any(p.startswith('tipos/') for p in paths):
        return 'tipos'
    if any(p.startswith('.github/') for p in paths):
        return 'ci'
    if any(p.startswith('scripts/') for p in paths):
        return 'scripts'
    return None


def build_message(adds, mods, dels):
    """Build conventional commit message from file changes."""
    all_paths = adds + mods + dels
    scope = determine_scope(all_paths)
    ctype = 'chore'
    if adds and not mods and not dels:
        ctype = 'feat'
    elif mods and not adds and not dels:
        # if python files changed, prefer fix, else chore
        if any(p.endswith('.py') for p in mods):
            ctype = 'fix'
        else:
            ctype = 'chore'
    elif dels and not adds and not mods:
        ctype = 'chore'

    if ctype == 'feat':
        desc = 'Add ' + ', '.join(adds[:4]) + \
            ('' if len(adds) <= 4 else ', ...')
    elif ctype == 'fix':
        desc = 'Modify ' + \
            ', '.join(mods[:4]) + ('' if len(mods) <= 4 else ', ...')
    else:
        sample = (adds + mods + dels)[:6]
        desc = 'Update ' + ', '.join(sample) + \
            ('' if len(all_paths) <= 6 else ', ...')

    header = ctype
    if scope:
        header += f"({scope})"
    header += f": {desc}"

    files_list = '\n\n' + \
        '\n'.join(['- ' + p for p in all_paths]) if all_paths else ''
    return header + files_list


def main():
    """Entry point: generate commit message from staged files."""
    if len(sys.argv) < 2:
        print('Usage: generate_commit_message.py <path-to-commit-msg-file>')
        raise SystemExit(2)

    commit_file = Path(sys.argv[1])
    # Get staged changes
    lines = staged_name_status()
    if not lines:
        # nothing staged — nothing to write
        raise SystemExit(0)

    adds, mods, dels = categorize(lines)
    message = build_message(adds, mods, dels)

    existing = commit_file.read_text(
        encoding='utf-8') if commit_file.exists() else ''
    if (existing.strip() == '' or all(
            l.strip().startswith('#') or l.strip() == ''
            for l in existing.splitlines())):
        commit_file.write_text(message + '\n', encoding='utf-8')
        print('Generated commit message written to', commit_file)
    else:
        print('Commit message already present; not overwriting')


if __name__ == '__main__':
    main()
