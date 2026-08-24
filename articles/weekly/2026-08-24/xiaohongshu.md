---
title: SDK升级别先改版本号
tags: [Claude, Python, SDK升级, AIAgent]
images: []
---

Anthropic Python SDK 0.x→1.x，最容易踩的坑不是装不上，而是“能 import，但边界行为已经变了”。

skills-zh 本周对齐上游 3b3fad9，给 claude-api 加入 upgrade 流程：

1️⃣ 先确认改动范围，依赖、lockfile、CI 一起纳入；
2️⃣ 用 inventory 搜 httpx、with_raw_response、旧 Completions、sampling 参数和 Bedrock；
3️⃣ 分开处理必改项与用户决策；
4️⃣ 改完重跑搜索、compileall、类型检查和测试；
5️⃣ 报告没验证到的部分，不用“应该兼容”糊过去。

2026-08-24 实测：
anthropic 1.0.0 已发布；
隔离安装要求 Python ≥3.10；
依赖 httpx2 2.12.0；
import 与 pip check 通过。

同一批变化还新增：

academy-guide：只在用户真想学 Claude 时推荐实时课程，做任务中途不打扰；

discernment-nudge：可行动回答后最多一次追加 2–3 个具体核对问题，用户已要求查证时不重复提醒。

仓库门禁已覆盖 19 个中文 Skill、三个分发包、Python/Shell 语法和上游事实文件一致性。

边界：没有拿真实 0.x 项目跑端到端升级，没有调用 Claude API，也没有做模型触发 A/B。

#Claude #Python #SDK升级 #AIAgent
