---
title: 大家会把 Agent 的美元预算、geo 和仓库 Skills 放在哪一层验收？
node: programmer
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

这周同步 Anthropic skills 的 `claude-api` 时，遇到一个比“API 参数怎么写”更有意思的问题：Agent 的成本、数据驻留和指令信任边界，应该由应用代码、平台能力还是 Skill 入口负责提醒？

上游 `f17010c` 给 Managed Agents 补了几组相关能力：session/deployment 的美元预算、`budget_reached` 暂停与恢复、`model.inference_geo`、仓库根目录 `.claude/skills` 自动发现、Advisor，以及更具体的 multiagent 分工建议。

几个边界很容易写错：

1. Session budget 是美元硬上限，不是 Messages API 的 token 型 `task_budget`；到上限后普通消息不能恢复，只能修改或移除预算。
2. Session budget 移除后不能重新加，deployment budget 却可以清除后再加。
3. Managed Agents 的 geo 在 `model` 对象里，multiagent roster 必须一致。
4. 仓库 Skills 会在 cloud session 启动时加载，所以仓库写权限也是 Agent 指令权限。

skills-zh 这次保留 17 个事实性 reference 与上游一致，只在中文入口补真实任务路由和近似反例。仓库 validator、quick validate、Python/Shell 语法和 Skill 打包都通过；因为上游只是 reference 更新，没有调用真实 beta API，所以没有把线上行为写成已实测。

我现在更倾向于把这类能力做成双层门禁：reference 保证参数与状态机准确，中文 Skill 负责在“每次最多花 25 美元”“主从 Agent 都要 US inference”“仓库里已经有 Skills”这样的自然任务里提醒正确边界。

大家在 Agent 平台落地时，会把预算和数据驻留验收放在 SDK 封装、部署策略，还是 prompt/skill 的任务路由里？有没有遇到 budget 达到后恢复或多 Agent geo 不一致的实际事故？

项目：https://github.com/MarcelLeon/skills-zh
