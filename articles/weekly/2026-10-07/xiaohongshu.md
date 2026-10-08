---
title: 从教程搭Agent先别急着复制
tags: [Claude, AIAgent, 开发安全, ManagedAgents]
images: []
---

看到一篇 Agent 教程，最危险的动作不是“看不懂”，而是直接复制 prompt、脚本、MCP 地址和定时任务。

这周 skills-zh 同步了 Managed Agents 两条上手路径：

1️⃣ quickstart 只匹配仓库里真实存在的模板，不猜名字、不拼路径；
2️⃣ URL 先分官方与第三方来源；第三方只复用设计，不复制 prompt、域名和包；
3️⃣ 页面永远是数据，不是给 Agent 的指令，里面的脚本不会直接运行；
4️⃣ 写文件前先展示文件树、外部写路径、凭据去向和 schedule；
5️⃣ `ant apply` 先 dry-run，真正 apply 再确认；deployment 创建后先暂停。

本轮中文入口新增 2 个真实场景和 3 条子命令路由；9 个模板结构、19 个正例/8 个反例、仓库 validator、打包和语法检查通过。

本机没有 `ant` CLI 和测试工作区，所以没有把本地验证说成真实平台交付。

#Claude #AIAgent #开发安全 #ManagedAgents
