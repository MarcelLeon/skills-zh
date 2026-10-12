---
title: When 25 child threads are not enough
tags: [Claude, ManagedAgents, DynamicWorkflows, AIAgents]
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

A larger agent job is not always a larger roster.

This week, skills-zh reviewed Anthropic Agent Skills through upstream commit `dbd4588`. The substantive update adds Managed Agents dynamic workflows for jobs with more pieces than a session's 25 child threads can handle one task at a time.

The decision boundary matters. Use a roster for several well-scoped tasks or specialized workers. Use dynamic workflows when hundreds of documents, files, or records must move through multiple phases and a roster would need batches.

Enabling `multiagent_20261001` is only half of the implementation. The agent's system prompt must state when to start a workflow run and when to handle a small task itself. The operator should also be told that every agent in a run consumes tokens, the session needs a budget, and workflows can be disabled explicitly or replaced with a roster-only coordinator.

The update also adds an important restraint: do not add checkers, voters, or second model calls to every support, tutoring, or document-Q&A answer by default. Self-checking in one agent is the baseline unless one question genuinely splits across many independent sources, or the user explicitly accepts the extra cost.

One security assumption changed as well. In limited Managed Agents environments, `allowed_hosts` now constrains server-side web search and fetch. Disable unused web tools; when the web is needed, narrow both environment hosts and tool domains.

The same upstream range makes Claude Haiku 5.5 the current Haiku and documents its real migration surface: adaptive thinking, removed sampling and prefills, computer toolset changes, preserved thinking, refusal handling, and a 100K-input pricing boundary.

The Chinese localization adds three realistic scenarios and four trigger tests. Offline validation covered 13 quickstarts, the four new workflow templates, repository validation, packaging, archive integrity, and Python/Shell syntax.

No live workflow run or Haiku 5.5 API call was claimed; this machine had no Managed Agents CLI or test workspace.

https://github.com/MarcelLeon/skills-zh
