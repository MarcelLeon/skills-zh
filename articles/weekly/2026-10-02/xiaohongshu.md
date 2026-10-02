---
title: 调Agent别再只挑成功案例
tags: [Claude, AIAgent, Prompt工程, 开发测试]
images: []
---

Agent 改完 Prompt，挑 3 个成功回答截图，不等于质量真的提升。

这周 skills-zh 同步了 Claude 应用的 eval 闭环：

1️⃣ 先定真实输入、生产 runner、grader；
2️⃣ 先审计 case / harness / metrics / grader；
3️⃣ train 找问题，validation 选方案，test 保持独立；
4️⃣ 每轮只改一个变量，记录分数、token、费用和失败样本；
5️⃣ 真实 API 运行前，先测单次成本并确认预算。

同一轮还补了 Opus 5.5 / Sonnet 5.5 迁移、preserved-thinking 前缀排查，以及大工具参数的 eager input streaming 校验。

重点不是“新模型更强”，而是把每次变化变成可复现、可比较、能停止的实验。

本地 19 个 Skill validator、打包、语法、路由、上游事实内容一致性和文章 payload 已通过；上游文件另有 16 处纯空白归一化。没有预算确认，不跑付费 eval，也不把文档同步说成线上效果提升。

#Claude #AIAgent #Prompt工程 #开发测试
