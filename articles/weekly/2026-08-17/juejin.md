---
title: Prompt 清理不能靠删字：一套带 findings 和 diff 的模型迁移审计
category: 人工智能
tags: [Claude, Prompt工程, Agent, 开发工具]
summary: 从 Prompt surface、Git provenance、keep list 到 proposed diff，介绍可验证的旧模型提示词审计。
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

# Prompt 清理不能靠删字：一套带 findings 和 diff 的模型迁移审计

模型升级后，代码里的 model ID 和参数容易被看见，Prompt 里的历史补丁却不会主动报错。

skills-zh 本周对齐 Anthropic `f6656c1`，在 `claude-api` 中接入 `prompt-audit`。它不按字符数评价 Prompt，而是要求每次删除都能对应到一个已命名的 dated pattern，并说明为什么不再适合目标模型。

## 审计先解决三个问题

第一，范围是什么。System prompt、工具描述、Skill、few-shot、模型参数和请求构造代码都可能影响模型行为，不能只找文件名里含 prompt 的内容。

第二，目标模型是什么。同一句 workaround 在旧模型上可能是必要约束，在新模型上可能导致过度触发或过度规划。审计会从请求、迁移文档和仓库配置推断目标，并把假设写在报告开头。

第三，为什么存在。仓库有 Git 历史时，结合 blame 判断强调、禁止和脚手架最初修复了什么失败，以及失败是否仍能复现。

## Findings 不是模糊建议

每条 finding 必须包含：

- `file:line` 与原文证据；
- 命中的模式；
- 面向目标模型的过时理由；
- 高、中、低置信度；
- remove、rewrite、move、replace-with-API-feature、add 或 flag。

高/中置信度项进入 proposed diff，低置信度只报告。一个 finding 一个 hunk，方便团队选择性接受和做行为归因。

## 删什么，也要写清楚不删什么

业务上下文、质量标准、工具契约、合规边界和脆弱操作的精确顺序不是 cruft。工具描述甚至可能需要补充，而不是缩短。没有证据的“看起来啰嗦”不能成为删除理由。

## 中文本土化的验收面

我们没有用英文 `SKILL.md` 覆盖中文入口。中文 description 增加“提示词是否过时”“清理 prompt cruft”“旧 Skill/tool description 审计”等自然触发；正文加入客服 Prompt 清理、模型迁移收尾两个 few-shot，并补 2 个正例和 1 个翻译型近似反例。

复现：

```bash
python3 scripts/validate_repository.py
python3 skills/skill-creator/scripts/quick_validate.py skills/claude-api
PYTHONPATH=skills/skill-creator python3 -m scripts.package_skill skills/claude-api /tmp/skill-dist
```

本轮仓库 validator 通过 17 个本土化 Skill，`claude-api` quick validate、打包、Python/Shell 语法、上游 reference 一致性和平台 payload 均通过。

边界也很明确：这些门禁只证明同步和路由结构正确；具体删改是否改善目标模型行为，仍要用 before/after probe 验证。

项目：https://github.com/MarcelLeon/skills-zh
