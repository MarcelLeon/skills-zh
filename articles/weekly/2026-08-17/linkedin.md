---
title: Prompt debt needs an audit trail, not a shorter word count
tags: [Claude, PromptEngineering, AIAgents, DeveloperTools]
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

Model migrations rarely stop at the model ID.

Prompts, skills, tool descriptions, few-shot examples, and request builders often retain workarounds added for older models: pressure language, rigid planning scripts, assistant prefills, JSON-forcing retries, and stale configuration.

This week skills-zh reviewed Anthropic upstream commit f6656c1 and localized the new claude-api prompt-audit workflow.

The useful distinction is not “long versus short.” Every finding must identify a dated pattern, cite file:line evidence, explain why it is obsolete for the target model, assign confidence, and propose an action. The workflow produces both a findings report and a proposed diff. Low-confidence observations stay out of the diff.

The keep list matters just as much: business context, quality bars, tool contracts, fragile operational sequences, and constraints that still reproduce remain load-bearing content.

For Chinese users, we added natural routing for two real tasks: cleaning up a customer-service prompt accumulated since Claude 3.5, and finishing an Opus 5 migration by auditing prefills and tool descriptions. Trigger evals include adjacent translation-only work that should not invoke the audit.

Repository validation passed for all 17 localized skills. The claude-api package, Python and shell syntax, upstream-reference parity, deterministic routing smoke test, and six channel payloads also passed.

These checks cannot prove that a contested deletion improves behavior; that still requires before/after probes on the target model.

https://github.com/MarcelLeon/skills-zh
