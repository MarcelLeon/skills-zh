#!/usr/bin/env python3
"""Summarize upstream changes since the recorded skills-zh baseline."""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE_FILE = ROOT / "sync" / "upstream-baseline.json"
RISK_WORDS = ("security", "unsafe", "symlink", "path traversal", "corrupt", "validation", "credential")


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.rstrip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", help="Base commit; defaults to sync/upstream-baseline.json")
    parser.add_argument("--head", default="upstream/main")
    parser.add_argument("--output", type=Path, help="Optional Markdown report path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    baseline = json.loads(BASELINE_FILE.read_text(encoding="utf-8"))
    base = args.base or baseline["reviewed_commit"]
    head = git("rev-parse", args.head)
    commits_raw = git("log", "--date=short", "--format=%h%x09%ad%x09%s", f"{base}..{head}")
    changes_raw = git("diff", "--name-status", f"{base}..{head}")

    by_skill: dict[str, list[str]] = defaultdict(list)
    other: list[str] = []
    for line in changes_raw.splitlines():
        if not line:
            continue
        fields = line.split("\t")
        path = fields[-1]
        if path.startswith("skills/") and len(path.split("/")) > 2:
            by_skill[path.split("/")[1]].append(line)
        else:
            other.append(line)

    risk_commits = [
        line for line in commits_raw.splitlines() if any(word in line.lower() for word in RISK_WORDS)
    ]
    lines = [
        "# Upstream Diff Report",
        "",
        f"- Base: `{base}`",
        f"- Head: `{head}`",
        f"- Commits: {len(commits_raw.splitlines()) if commits_raw else 0}",
        "",
        "## Changed skills",
        "",
    ]
    if by_skill:
        lines.extend(f"- `{name}`: {len(items)} files" for name, items in sorted(by_skill.items()))
    else:
        lines.append("- No skill changes.")

    lines.extend(["", "## Risk-related commits", ""])
    lines.extend(f"- {line}" for line in risk_commits)
    if not risk_commits:
        lines.append("- No risk keyword hits; manual review is still required.")

    lines.extend(["", "## Commits", ""])
    lines.append("```text")
    lines.append(commits_raw or "No new commits.")
    lines.append("```")
    if other:
        lines.extend(["", "## Other paths", "", "```text", *other, "```"])

    report = "\n".join(lines) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
        print(output)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
