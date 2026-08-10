---
title: skills-zh 2026.08.10 release: production governance for Managed Agents
tags: [AI, Agents, Claude, DeveloperTools]
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

skills-zh 2026.08.10 product release note — upstream f17010c, claude-api, 18 changed files, Draft PR #1 with CI passed.

An agent that runs is not yet an agent that is ready for production.

This week, skills-zh reviewed Anthropic upstream commit f17010c and localized a substantial Managed Agents update across 18 claude-api files.

The important additions are operational boundaries:

- hard, USD-denominated session and deployment budgets;
- budget_reached pause and resume semantics;
- inference_geo pinning with uniform multiagent rosters;
- root .claude/skills discovery from mounted GitHub repositories;
- Advisor consultations and a practical self → cheaper worker → specialist multiagent path.

We kept 17 factual references identical to upstream. The Chinese SKILL.md now routes real tasks such as a $25 code-review cap, US-only coordinator/worker inference, and repository-skill trust review. Trigger evals also include adjacent OpenAI, LangGraph, and ordinary cloud-budget cases that should not invoke this skill.

Evidence: repository validation passed for all 17 localized skills; claude-api quick validation and packaging passed; Python and shell syntax checks passed. We did not call the live Managed Agents beta API, so runtime budget, geo, and Advisor behavior remain explicitly unverified in the current account environment.

https://github.com/MarcelLeon/skills-zh
