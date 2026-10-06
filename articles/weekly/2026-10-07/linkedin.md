---
title: Treat agent onboarding pages as data, not instructions
tags: [Claude, ManagedAgents, AIAgents, DeveloperTools]
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

Turning a quickstart or a blog post into a managed agent is not primarily a copy-and-paste task. It is a provenance, credential, and change-control task.

This week, skills-zh reviewed Anthropic Agent Skills through upstream commit `683bc88`. The substantive update adds two Managed Agents onboarding paths: build from a bundled quickstart name, or derive a version-controlled setup from a URL.

Bundled quickstarts must match a real filename or `console_key`; unknown names are listed, not guessed. The flow remains staged: agent, environment, vault, test session, schedule, and integration.

URL onboarding uses five steps: fetch, extract, propose, write, and apply. Anthropic's explicitly allowed first-party sources may preserve their content. Third-party pages contribute design only; prompts, names, files, hosts, and packages are rebuilt and independently verified.

In both tiers, the page is data, not instructions. Its scripts are not executed. The proposal must expose the file tree, external write paths, credential recipients, least-privilege scope, schedule, and unresolved placeholders before files are written.

Platform changes remain separate: run an `ant apply` walk check and dry-run, obtain approval for the actual apply, and pause a newly created deployment before it can run on schedule. Vault files describe containers, never secrets.

The Chinese localization adds two realistic examples, three onboarding routes, two positive trigger cases, and one adjacent negative case. Offline validation covered nine quickstart templates, 19 positive and eight negative Claude API routes, repository validation, packaging, archive integrity, and Python/Shell syntax.

No real agent, session, deployment, or MCP write was claimed: this machine did not have the `ant` CLI or a test Claude Platform workspace.

https://github.com/MarcelLeon/skills-zh
