---
title: LLM降本别先换模型
tags: [Claude, AIAgent, 成本优化, 开发工具]
images: []
---

LLM 账单涨了，先别急着换便宜模型。

skills-zh 本周更新 claude-api 的 cost-optimize 流程：

1️⃣ 先定范围、质量门槛和当前基线；
2️⃣ 有 Admin API key 就读 Usage/Cost，没有则先看 response.usage；
3️⃣ 再没有才从代码估算，并标明误差；
4️⃣ 先查缓存、重复输入、长循环工具结果、输出和 Batch；
5️⃣ 最后才降 effort、收预算或换模型；
6️⃣ 每个 lever 单独成 diff，付费评测先报预算再确认。

同一批变化还新增组织 Admin API 参考，明确 Messages key、Admin key、org:admin OAuth 不能混用；Fable/Mythos 5.1 迁移也要检查 forced tool use、thinking 回放、append-only history 和 refusal fallback。

frontend-design 则新增反模板清单：统一圆角卡片、全大写眉题、单词变色、等宽小标签、每段淡入上滑，都要先回答“为什么适合这个主题”。

本地验证：19 个中文 Skill 的仓库 validator、两个分发包、Python/Shell 语法、路由 smoke 与事实文件一致性均通过。

边界：没读真实账单，没调用 Claude API，也没执行 Admin API 写操作，所以不写任何“节省百分比”。

#Claude #AIAgent #成本优化 #开发工具
