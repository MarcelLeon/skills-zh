---
title: 从教程生成 Agent 配置时，你们怎么划分“可复制”的边界？
node: programmer
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

这周同步 Anthropic Agent Skills 的 `claude-api`，上游新增了两条 Managed Agents onboarding：按内置 quickstart 名称创建，或者从一个 URL 提取方案。

我觉得真正有价值的不是多了一个命令，而是把“页面里什么能复制”写成了边界。

内置 quickstart 必须精确匹配仓库里的文件名或 `console_key`，不匹配就列候选，不猜模板。URL 则先做来源分级：指南限定的 Anthropic 官方来源可以保留内容，第三方只复用角色、流程和完成标准，prompt、文件名、域名和包都重新写。

无论来源，页面都只是数据，不是指令。页面里的脚本不直接执行；每个 host、MCP URL、package 和凭据去向要从供应商官方来源独立核验。

写文件前还要先展示文件树、外部写路径、凭据表和 schedule，然后停下来等确认。平台侧先 `ant apply` dry-run，真正 apply 再确认；deployment 创建后立即 pause，避免定时任务先跑起来。

skills-zh 这轮保留 17 个事实性 reference/模板原文，只重写中文入口，新增 2 个 few-shot、2 个正例和 1 个近似反例。离线检查了 9 个模板的 frontmatter、文件名、`console_key` 和 agent 块；validator、打包和语法也通过。

限制也很明确：本机没有 `ant` CLI 和 Claude Platform 测试工作区，所以没有真实创建 Agent、session 或 deployment。

大家在做“从文档/博客生成 Agent 配置”时，会把哪些东西视为可复制事实，哪些必须重新验证或重写？对于官方 GitHub 仓库里可由外部贡献者修改的 prompt，你们会默认信任吗？

项目：https://github.com/MarcelLeon/skills-zh
