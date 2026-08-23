---
title: Prompt 不是越短越好：把旧模型遗留指令变成可审计 diff
tags: [Claude API, Prompt Engineering, Agent Skills, 开发工具]
categories: [AI]
links:
  - https://github.com/MarcelLeon/skills-zh
images: []
---

# Prompt 不是越短越好：把旧模型遗留指令变成可审计 diff

一个 Agent 的 system prompt 往往不是设计出来的，而是“长出来”的。

旧模型漏调用工具，就加一句 `MUST`；输出不稳定，就塞一个固定示例；JSON 解析失败，就补 assistant prefill、stop sequence 和重试。几年后模型、API 和业务都变了，仓库里却留下了每一代模型的补丁合集。

本周 skills-zh 对齐 Anthropic 上游 `f6656c1`，为 `claude-api` 新增 `prompt-audit`。这次只变化 3 个文件，却补出了一套很实用的判断框架：目标不是把 Prompt 改短，而是找出能被证据证明已经过时的指令，并把 findings 与 proposed diff 一起交付。

## 一、先盘点 Prompt surface，不只搜 prompt.txt

审计对象包括：

- system prompt 及其拼装代码；
- tools 数组中的工具和参数描述；
- `SKILL.md`、`CLAUDE.md` 等规则文件；
- 模型 ID、thinking、采样参数、stop sequence、prefill 和 retry 代码；
- few-shot 与嵌入式示例。

这一步很关键。比如“输出 ONLY valid JSON”可能只是表面，真正的旧机制还包含末尾 assistant prefill、正则抽取和 parse 失败后的重试。只改一句 Prompt，旧请求形状仍能从另一个分支发出去，应用并没有完成迁移。

## 二、过时与否取决于目标模型

`prompt-audit` 会从请求和仓库推断审计范围与目标模型，并把假设写在报告顶部。它还会利用 Git blame 追问：这句强调最初修复了哪个模型的什么失败？目标模型上还能复现吗？

审计覆盖四组问题：

1. 旧 Prompt 文本，如压力语言、被 API 特性替代的脚手架、过度步骤化和模型化石。
2. 脆弱 Skill，如把一次偶发失败永久写成规则、硬编码易漂移事实、不断累加近义触发短语。
3. 工具描述，如契约不足，或把行为训诫和 worked example 错塞进 description。
4. 请求配置与架构，如旧参数、cache-hostile 顺序、让 LLM 重复执行本可由代码确定完成的循环。

每一条 finding 都必须落到 `file:line`，说明命中的模式、为何对目标模型过时、置信度和建议行动。无法对应到明确模式和目标模型理由的内容，只能低置信度标记，不能直接进入修改 diff。

## 三、keep list 比删除表更重要

“Prompt 越短越好”是一个危险误区。业务受众、产品事实、质量标准、工具契约和失败模式，模型无法凭空知道；删除这些内容，只会让输出变得更通用、更保守。

因此上游明确保留：

- 只有作者掌握的业务上下文；
- 参数语义、限制和工具不会返回什么；
- 鉴权、删除、合规等脆弱操作的精确顺序；
- 在目标模型上仍能复现的禁止项；
- 真正需要固定格式的示例；
- 没有冲突且工作正常的重复契约。

一个干净的 Prompt surface 可以得到零 findings 和空 diff。审计不是为了制造删改数量。

## 四、中文入口如何避免“翻译完就算同步”

我们保留 219 行事实性 `shared/prompt-audit.md` 与上游一致，中文 `SKILL.md` 只负责把自然任务路由到正确事实来源。

新增的两个中文场景分别是：

1. 客服 Agent 的 system prompt 从 Claude 3.5 时代一直打补丁，希望先拿 findings 和 proposed diff，不直接改文件。
2. 从 Sonnet 4.6 迁移到 Opus 5 后，继续清理 assistant prefill、`think step by step` 和过度触发式工具描述。

触发评测同时加入近似反例：“只把系统提示词翻译成中文，原意和结构不变”不应被扩大为模型迁移或 Prompt 审计。

## 五、如何复现仓库验收

```bash
python3 scripts/upstream_diff_report.py
python3 scripts/validate_repository.py
python3 skills/skill-creator/scripts/quick_validate.py skills/claude-api
PYTHONPATH=skills/skill-creator python3 -m scripts.package_skill skills/claude-api /tmp/skill-dist
```

本轮仓库 validator 通过 17 个本土化 Skill，`claude-api` quick validate、打包、Python/Shell 语法、上游 reference 一致性和 6 个平台 payload 均通过。代表性 smoke 还验证了分发包包含 219 行 `prompt-audit.md`、中文入口以及 8 个正例和 4 个近似反例。

Prompt 行为本身仍需要在目标模型上对 contested change 做 before/after probe；文本规则通过 validator，不等于删除后一定没有回归。

项目地址：https://github.com/MarcelLeon/skills-zh
