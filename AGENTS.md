# Repository Guidelines

## Project Structure & Module Organization

This repository is a Chinese adaptation of Anthropic’s Agent Skills examples. Each independently usable skill lives in `skills/<skill-name>/` and must contain a `SKILL.md`. Keep supporting code, references, templates, fonts, and other assets inside that skill’s directory. Shared repository metadata is in `.claude-plugin/marketplace.json`; `template/SKILL.md` is the minimal starting point for a new skill, and `spec/` points contributors to the current Agent Skills specification.

## Build, Test, and Development Commands

There is no repository-wide build. Use Python 3.11, then validate and package the skill you changed:

```bash
python3 skills/skill-creator/scripts/quick_validate.py skills/<skill-name>
python3 skills/skill-creator/scripts/package_skill.py skills/<skill-name> /tmp/skill-dist
python3 scripts/validate_repository.py
python3 scripts/upstream_diff_report.py
python3 -m compileall skills/<skill-name>
find skills/<skill-name> -name '*.sh' -exec bash -n {} +
```

The repository validator also checks plugin paths, synchronization baselines, and Chinese trigger evals. Packaging creates a distributable `.skill` archive. Use syntax checks only when the skill contains relevant code.

## Coding Style & Naming Conventions

Use kebab-case for skill directories and frontmatter `name` values. Every `SKILL.md` begins with YAML frontmatter containing at least `name` and `description`. Follow `LOCALIZATION.md`: adapt Chinese colloquial triggers, work scenarios, few-shot examples, and near-miss cases instead of translating line by line. Preserve exact API names, commands, factual references, and upstream licenses. Use four spaces for Python and existing file-local shell style.

## Testing Guidelines

Run both validators for every changed skill and update `localization/trigger-evals.json`. Exercise changed scripts with representative Chinese inputs. Visually verify DOCX, PDF, PPTX, XLSX, HTML, and GIF outputs. Keep fixtures within the owning skill; name Python tests `test_*.py`.

## Commit & Pull Request Guidelines

Use `sync(<skill>): 对齐 upstream <sha> 并完成中文本土化` for upstream alignment and concise imperative subjects otherwise. PRs must list affected skills, upstream commits, localization decisions, and validation results. Add sample artifacts for visual changes and call out license, dependency, or retained-English-reference changes.
