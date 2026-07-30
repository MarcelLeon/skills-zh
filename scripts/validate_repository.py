#!/usr/bin/env python3
"""Repository-level checks for skills-zh."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
VALIDATOR = SKILLS_DIR / "skill-creator" / "scripts" / "quick_validate.py"
CJK_RE = re.compile(r"[\u3400-\u9fff]")
VALIDATOR_PYTHON = os.environ.get("SKILLS_ZH_VALIDATOR_PYTHON", sys.executable)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_frontmatter(skill_md: Path) -> dict[str, str]:
    content = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    lines = match.group(1).splitlines()
    result: dict[str, str] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        key_match = re.match(r"^(name|description):\s*(.*)$", line)
        if not key_match:
            index += 1
            continue
        key, value = key_match.groups()
        if value in {"|", "|-", ">", ">-"}:
            parts: list[str] = []
            index += 1
            while index < len(lines) and (lines[index].startswith("  ") or not lines[index].strip()):
                parts.append(lines[index].strip())
                index += 1
            result[key] = " ".join(parts).strip()
            continue
        result[key] = value.strip().strip("\"'")
        index += 1
    return result


def validate_skills(errors: list[str]) -> set[str]:
    names: set[str] = set()
    for skill_dir in sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir()):
        name = skill_dir.name
        names.add(name)
        result = subprocess.run(
            [VALIDATOR_PYTHON, str(VALIDATOR), str(skill_dir)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            fail(errors, f"{name}: quick_validate failed: {result.stdout.strip() or result.stderr.strip()}")
            continue

        skill_md = skill_dir / "SKILL.md"
        frontmatter = load_frontmatter(skill_md)
        if frontmatter.get("name") != name:
            fail(errors, f"{name}: frontmatter name must match directory")

        description = frontmatter.get("description", "")
        if not isinstance(description, str) or not CJK_RE.search(description):
            fail(errors, f"{name}: description must contain a Chinese trigger description")

        body = skill_md.read_text(encoding="utf-8")
        if len(CJK_RE.findall(body)) < 20:
            fail(errors, f"{name}: SKILL.md lacks a substantive Chinese entrypoint")
    return names


def validate_marketplace(errors: list[str], skill_names: set[str]) -> None:
    marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    listed: set[str] = set()
    for plugin in marketplace.get("plugins", []):
        for raw_path in plugin.get("skills", []):
            path = (ROOT / raw_path).resolve()
            if not path.is_dir():
                fail(errors, f"marketplace references missing directory: {raw_path}")
                continue
            listed.add(path.name)
    missing = skill_names - listed
    extra = listed - skill_names
    if missing:
        fail(errors, f"marketplace missing skills: {', '.join(sorted(missing))}")
    if extra:
        fail(errors, f"marketplace lists unknown skills: {', '.join(sorted(extra))}")


def validate_localization_evals(errors: list[str], skill_names: set[str]) -> None:
    data = json.loads((ROOT / "localization" / "trigger-evals.json").read_text(encoding="utf-8"))
    cases = data.get("skills", {})
    case_names = set(cases)
    if case_names != skill_names:
        missing = skill_names - case_names
        extra = case_names - skill_names
        if missing:
            fail(errors, f"trigger evals missing skills: {', '.join(sorted(missing))}")
        if extra:
            fail(errors, f"trigger evals contain unknown skills: {', '.join(sorted(extra))}")

    for name, item in sorted(cases.items()):
        positive = item.get("should_trigger", [])
        negative = item.get("should_not_trigger", [])
        if len(positive) < 2 or len(negative) < 1:
            fail(errors, f"{name}: needs >=2 should_trigger and >=1 should_not_trigger cases")
        for query in [*positive, *negative]:
            if not isinstance(query, str) or len(query.strip()) < 8 or not CJK_RE.search(query):
                fail(errors, f"{name}: eval query must be a realistic Chinese prompt: {query!r}")


def validate_sync_baseline(errors: list[str], skill_names: set[str]) -> None:
    baseline = json.loads((ROOT / "sync" / "upstream-baseline.json").read_text(encoding="utf-8"))
    reviewed = baseline.get("reviewed_commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", reviewed):
        fail(errors, "sync baseline reviewed_commit must be a full Git SHA")
    mapped = set(baseline.get("skills", {}))
    if mapped != skill_names:
        fail(errors, "sync baseline skill map must exactly match skills/")


def validate_readme(errors: list[str]) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "scripts/init_skill.py" in readme:
        fail(errors, "README references deleted scripts/init_skill.py")
    if "LOCALIZATION.md" not in readme or "UPSTREAM_SYNC.md" not in readme:
        fail(errors, "README must link localization and upstream-sync policies")


def main() -> int:
    errors: list[str] = []
    skill_names = validate_skills(errors)
    validate_marketplace(errors, skill_names)
    validate_localization_evals(errors, skill_names)
    validate_sync_baseline(errors, skill_names)
    validate_readme(errors)

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Repository validation passed: {len(skill_names)} localized skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
