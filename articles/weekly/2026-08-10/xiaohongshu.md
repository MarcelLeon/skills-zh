---
title: skills-zh周更：Agent治理升级
tags: [AIAgent, Claude, 开发者工具, 多Agent]
images:
  - assets/xhs/card-01.png
  - assets/xhs/card-02.png
  - assets/xhs/card-03.png
  - assets/xhs/card-04.png
  - assets/xhs/card-05.png
  - assets/xhs/card-06.png
  - assets/xhs/card-07.png
---

skills-zh 2026.08.10 周更新发布：这次不追新模型，补的是 Agent 进入生产前的治理边界。

本期对齐 Anthropic 上游 f17010c，claude-api 共 18 个文件变化：

1️⃣ Managed Agents 的 session budget 是美元硬上限，不是 Messages API 的 token 型 task_budget。到 budget_reached 后，普通消息不能恢复，只能修改或移除预算。

2️⃣ session budget 移除后不能再加；deployment budget 可以清除后重新加入。

3️⃣ Managed Agents 的 inference_geo 写在 model 里。Coordinator、worker、Advisor 要统一 geo，不能各配各的。

4️⃣ cloud session 会在启动时加载仓库根目录 .claude/skills。方便版本管理，也意味着能改这个目录的人能改 Agent 指令，外部 PR 必须审计。

中文本土化不是逐句翻译：17 个事实 reference 保持上游原样，中文入口新增“25 美元代码审查预算”“主从 Agent 固定 US inference”“仓库 Skills 安全边界”等真实任务和近似反例。

交付状态：17 个 Skill 仓库门禁、打包、Python/Shell 语法、文章 payload 和远端 CI 全部通过。

边界说明：没有调用真实 Managed Agents beta API，所以预算暂停、geo pin 和 Advisor 仍标记为当前账号未实测。

#AIAgent #Claude #开发者工具 #多Agent
