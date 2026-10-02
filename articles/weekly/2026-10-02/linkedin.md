---
title: Turn Claude prompt tuning into an auditable eval loop
tags: [Claude, AIAgents, Evaluation, DeveloperTools]
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

Picking a few successful outputs after a prompt change is not an evaluation strategy.

This week, skills-zh reviewed Anthropic Agent Skills through upstream commit `8a1541c` and localized a substantive Claude API update around evals and iterative improvement.

The new workflow treats an eval as three connected parts: representative inputs, a runner that exercises the real application path, and a grader that measures the behavior users actually care about. Before a paid run, the inputs, grading method, and measured budget must be approved.

An eval audit comes first. It checks task coverage, harness fidelity, metric hygiene, grader leakage, and whether the suite can detect the intended change.

Hill-climbing then uses a train/validation/test split. Each round records the single change, quality scores, token and cost data, failures, and a stopping condition. The held-out test set is evidence, not another prompt-tuning input. The upstream package also includes a report schema, a lightweight HTML report builder, and a runner scaffold.

The same update adds Claude Opus 5.5 and Sonnet 5.5 migration guidance, preserved-thinking migration diagnostics, and safer eager input streaming for large client-tool payloads. These are not string-replacement migrations: thinking/effort, forced tool use, conversation-prefix integrity, schema validation, and platform availability all need explicit checks.

Scope: 2 upstream commits, 1 skill, 72 files, +6,982/-620. Repository validation passed for 19 localized skills, along with packaging, Python/Shell/Node syntax, 17 positive and 7 negative Chinese routes, factual-content parity (plus 16 whitespace-only normalizations), offline diagnostic/report smoke tests, and six publication payloads.

No paid Claude API eval, hillclimb, or replay was run without an approved budget. Local validation is not production proof.

https://github.com/MarcelLeon/skills-zh
