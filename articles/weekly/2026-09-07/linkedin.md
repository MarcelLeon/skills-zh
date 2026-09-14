---
title: Cost optimization starts with a token profile
tags: [Claude, AIAgents, CostOptimization, DeveloperTools]
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

LLM cost optimization should not begin with a cheaper model. It should begin with a baseline.

This week, skills-zh reviewed Anthropic Agent Skills through upstream commit 41bbe19 and localized two substantive changes across claude-api and frontend-design.

The new claude-api cost-optimize route creates an evidence chain:

- establish scope, quality bar, and cost per completed task;
- use Usage/Cost Admin API data when available, application response.usage logs next, and code estimates only as the fallback;
- rank levers by savings ceiling;
- apply free wins first: caching, input hygiene, agent-loop hygiene, output control, and batch;
- treat effort, budgets, model selection, and multi-model routing as quality trade-offs;
- isolate every lever in its own diff and keep or revert it against the same evaluation set;
- estimate spend and get approval before any paid model run.

The upstream package also adds an Admin API reference for members, workspaces, API keys, rate limits, service accounts, WIF, and CMEK. The Chinese route explicitly separates Messages API keys, Admin API keys, and org:admin OAuth, then starts from least privilege and dry-run or read-only plans.

Fable/Mythos 5.1 migration is routed beyond a model-id swap: forced tool use, append-only history, thinking-block replay, refusal fallbacks, retention, streaming, timeouts, and platform availability all need inspection.

frontend-design now turns common generated-page defaults into review questions: identical rounded cards, all-caps eyebrow labels, one-word headline accents, monospace micro-labels, decorative arrows, and repeated fade-slide animations. They are not banned; they need a reason grounded in the actual subject.

Evidence: repository validation passed for 19 localized skills. Both changed skills passed quick validation, packaging, ZIP integrity, Python and shell syntax checks, routing smoke tests, and factual-reference parity.

Limit: we did not call the Claude API, access real organization billing, execute Admin API writes, or run model-level trigger A/B tests. No savings claim is being made.

https://github.com/MarcelLeon/skills-zh
