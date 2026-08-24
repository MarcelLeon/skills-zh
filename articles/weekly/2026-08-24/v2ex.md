---
title: SDK major upgrade 里，哪些决定不应该让 Agent 自动做？
node: programmer
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

最近同步 Anthropic Agent Skills 的 `claude-api`，上游新增了一份 Python `anthropic` SDK 0.x→1.x 升级指南。

我比较喜欢的不是 breaking changes 数量，而是它把迁移项分成两类：

1. `[BREAKS]`：可以从代码和新 API 直接证明必须改，例如 SDK 边界上的 `httpx` 对象切到 `httpx2`、async `with_raw_response` 读 body 需要 `await`、Text Completions 移除。
2. `[DECIDE]`：证据只能把问题暴露出来，最终选择属于项目负责人，例如 Python 3.10 floor、局部 import 还是进程级 `alias_httpx()`、旧采样参数是否仍承载业务语义、Bedrock region 应该是什么。

它还要求先确认范围。`upgrade python` 没带路径时，不能直接扫完整个工作区；代码一旦进入范围，根目录依赖和 lockfile 才随之纳入。完成后重跑同一份 inventory，每个残余命中都要说明为什么保留，再跑 compileall、项目已有的类型检查和测试。

2026-08-24 我实际查到 `anthropic 1.0.0` 已发布，并在一次性 Python 3.11 环境装过：包元数据是 `Requires-Python >=3.10`，依赖 `httpx2 2.12.0`，import 和 `pip check` 通过。但这只能证明发行包与指南的几个关键前提，不能代替一个真实 0.x 项目的端到端迁移。

这周还新增两个很强调“不要越界”的 Skill：

- `academy-guide`：只有用户想学习 Claude 产品时才推荐实时 Academy 内容；任务执行中不插入课程。
- `discernment-nudge`：可行动回答后最多一次追加具体反思问题；用户已经要求核验时不再让他“自行检查”。

中文本土化给三个变化 Skill 都补了真实 few-shot 和相邻反例。仓库 validator、分发包、Python/Shell 语法、upstream reference parity 已过；没有做模型触发 A/B，也没有跑真实项目迁移。

大家在做自动化 SDK 升级时，通常怎么划“Agent 可以直接改”和“必须把决定交回给 owner”的边界？Python/Node/Java 的规则会放在同一个 codemod，还是每个 SDK 单独维护 migration playbook？

项目：https://github.com/MarcelLeon/skills-zh
