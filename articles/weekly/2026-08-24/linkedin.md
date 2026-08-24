---
title: Major SDK upgrades need an evidence chain, not a version bump
tags: [Claude, Python, SDKMigration, AIAgents]
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

A major SDK upgrade should not begin with editing the dependency pin. It should begin with scope.

This week, skills-zh reviewed Anthropic Agent Skills through upstream commit 3b3fad9 and localized three capability changes.

The main addition is the claude-api upgrade workflow for the Python anthropic SDK, from 0.x to 1.x. It turns migration into an executable evidence chain:

- confirm the files, directories, manifests, and lockfiles in scope;
- verify that a 1.x release actually exists before writing an exact pin;
- inventory Python floors, httpx objects crossing the SDK boundary, raw responses, Text Completions, removed parameters, compaction, and Bedrock clients;
- separate mechanical BREAKS from owner decisions;
- rerun the inventory, type checks, tests, and compile checks;
- report every remaining limitation.

On 2026-08-24, we verified that anthropic 1.0.0 was published. A clean Python 3.11 environment installed it successfully and confirmed Requires-Python >=3.10, httpx2 2.12.0, a working anthropic.Timeout import, and a clean dependency check.

Two new skills reinforce the same boundary discipline.

academy-guide recommends live Claude Academy resources only when the user is trying to learn a Claude product. It stays quiet during task execution and never invents a catalog item.

discernment-nudge adds two or three specific reflection questions after an actionable answer, at most once per conversation. It skips code, formatting, educational explanations, creative work, and requests that already asked for verification.

For Chinese users, we rewrote the trigger descriptions, added two realistic few-shot scenarios per changed skill, and added adjacent negative cases. Repository validation passed for 19 localized skills, all three distributable packages, Python and shell syntax, and upstream factual-file parity.

Limits matter: we did not run an end-to-end migration against a real 0.x application, call the Claude API, or run model-level trigger A/B tests. The Academy site was reachable, but the CLI catalog JSON fetch timed out, so no live item-selection claim is included.

https://github.com/MarcelLeon/skills-zh
