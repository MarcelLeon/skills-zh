---
title: Agent预算不是token提醒
tags: [AIAgent, Claude, 开发者工具, 多Agent]
images: []
---

Agent 能跑，不等于能放心进生产。

这周同步 Anthropic claude-api，我重点补了 4 个容易混淆的边界：

1️⃣ Managed Agents 的 session budget 是美元硬上限，不是 Messages API 的 token 型 task_budget。到 budget_reached 后，普通消息不能恢复，只能修改或移除预算。

2️⃣ session budget 移除后不能再加；deployment budget 可以清除后重新加入。

3️⃣ Managed Agents 的 inference_geo 写在 model 里。Coordinator、worker、Advisor 要统一 geo，不能各配各的。

4️⃣ cloud session 会在启动时加载仓库根目录 .claude/skills。方便版本管理，也意味着能改这个目录的人能改 Agent 指令，外部 PR 必须审计。

中文本土化不是把英文逐句翻掉：事实 reference 保持上游原样，中文入口新增“25 美元代码审查预算”“主从 Agent 固定 US inference”“仓库 Skills 安全边界”等真实任务和近似反例。

验证结果：17 个 Skill 仓库门禁、claude-api 打包、Python/Shell 语法通过。没有调用真实 beta API，所以我没有写成线上已实测。

#AIAgent #Claude #开发者工具 #多Agent
