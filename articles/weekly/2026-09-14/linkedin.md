---
title: Auto permission is not a human checkpoint
tags: [Claude, AIAgents, Security, DeveloperTools]
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

An `auto` tool-permission policy does not mean every call waits for a human.

This week, skills-zh reviewed Anthropic Agent Skills through upstream commit 34040c9 and localized one substantive Claude API update.

Managed Agents `auto` evaluates each server-executed tool call and produces one of three outcomes:

- `allow`: the call runs immediately;
- `ask`: the session pauses for `user.tool_confirmation`;
- `deny`: the high-risk call does not run, the agent receives an error result, and the session continues.

The client therefore needs to branch on each `agent.tool_use` or `agent.mcp_tool_use` event's `evaluated_permission`, not on the configured policy. It should only confirm `ask` events, preserve `evaluation.type` and `reason_code` for audit, tolerate unknown enum values, and use `deny_message` for a human denial reason.

There is also a trust-boundary detail: text sent by the application as `user.message` is treated as application intent during evaluation, even when the application relays untrusted end-user text. If a person must inspect a tool call before it runs, that tool still needs `always_ask`.

The update also documents `ant beta:sessions connect`. Its terminal view follows the primary thread and supports messages, interrupts, and pending approvals. The `--web` viewer runs locally and can show every thread in a multi-agent session. Non-interactive clients should keep using the events APIs.

Evidence: repository validation passed for 19 localized skills. Claude API quick validation, packaging, ZIP integrity, Python and shell syntax, route smoke tests, and exact Git-blob parity for six factual references all passed.

Limit: this machine has no `ant` CLI or test session. We did not run `connect`, exercise the three server-side `auto` outcomes, or call the Claude API.

https://github.com/MarcelLeon/skills-zh
