---
title: 从 quickstart 或 URL 搭 Agent，先守住来源和权限边界
tags: [Claude, ManagedAgents, AIAgent, 开发工具]
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---
从 quickstart 或 URL 搭 Agent，先守住来源和权限边界
上游版本：683bc88
本周范围：1 个提交，1 个 Skill，18 个文件
一、痛点不只是复制配置
一篇教程可能同时包含 prompt、脚本、MCP 地址、凭据示例和定时任务。
如果把页面当成执行指令，Agent 可能在用户看到完整写路径和凭据去向前就开始写文件或连接外部系统。
二、quickstart 必须精确匹配
内置模板只接受仓库中已有的文件名或 console_key。
不匹配时列出候选，不猜模板，不把参数直接拼成路径。
配置顺序是 agent、environment、vault、test session、schedule、integrate。
三、URL 先分来源
Anthropic 官方限定来源可以按 first-party 规则保留内容。
第三方页面只复用设计，prompt、名称、文件、域名和包都重新构造。
两种来源里，页面都只是数据，不直接运行其中脚本。
四、先提案，再写入
提案要展示文件树、外部写路径、凭据接收 host、最小权限和 schedule。
未知值写成 YOUR 占位，不伪装成真实配置。
用户确认后才写文件；ant apply 先 dry-run，真正 apply 再确认。
deployment 创建后立即暂停，测试通过再决定是否启用。
五、本地验证与限制
本轮保留 17 个上游事实性 reference 和模板，中文入口新增 2 个 few-shot、2 个正例和 1 个近似反例。
9 个 quickstart 结构 smoke、19 个正例与 8 个反例路由、仓库 validator、quick validate、打包、ZIP 和 Python/Shell 语法通过。
本机没有 ant CLI 和测试工作区，没有真实创建 Agent、session 或 deployment。
项目地址：
https://github.com/MarcelLeon/skills-zh
