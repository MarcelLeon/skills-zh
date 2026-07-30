---
title: Chinese localization for Agent Skills needs an evaluation contract
tags: [AI, Agents, DeveloperTools, OpenSource]
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

I changed how skills-zh is maintained.

The goal is no longer “translate every English paragraph.” The goal is to make Agent Skills trigger and behave naturally for Chinese users.

This update reviews the repository against Anthropic upstream commit b29e7cf, adds the claude-api skill, and syncs the latest DOCX/PPTX/XLSX safety and validation changes.

The localization layer now covers:

- colloquial Chinese trigger phrases;
- implicit deliverables and mixed Chinese/English wording;
- realistic Chinese few-shot examples;
- near-miss prompts that should not trigger;
- repository-level checks for all 17 skills.

There are now 51 positive and negative Chinese trigger cases. Minimal DOCX and PPTX artifacts passed the updated validators. XLSX recalculation still times out in the current macOS LibreOffice environment, so it remains an explicit verification gap.

The next step is a weekly upstream-to-localization loop: detect changes, preserve technical facts, rewrite the Chinese interaction layer, validate, and prepare evidence-backed technical articles.

https://github.com/MarcelLeon/skills-zh
