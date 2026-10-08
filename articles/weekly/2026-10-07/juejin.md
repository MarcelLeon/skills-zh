---
title: 从 URL 搭 Managed Agent，为什么必须先做来源分级
category: 人工智能
tags: [Claude, Agent, 安全, 开发工具]
summary: quickstart 与 URL onboarding 的关键不是复制配置，而是控制来源、凭据、写入和部署生效边界。
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

# 从 URL 搭 Managed Agent，为什么必须先做来源分级

“照这个教程搭一个 Agent”经常被理解成配置复制。可一旦 Agent 能读取外部页面、拿到 MCP 凭据并定时运行，复制边界就变成安全边界。

Anthropic Agent Skills 上游 `683bc88` 为 `claude-api` 新增 quickstart 名称和 URL 两种 Managed Agents onboarding。skills-zh 本轮保留上游事实 reference，重写中文触发与验收路径。

## quickstart 必须精确匹配

内置模板只接受 `shared/managed-agents-quickstarts/` 已有文件名或 `console_key`。不匹配就列出候选，不把用户输入拼成路径，也不凭记忆生成模板。

匹配后按 agent、environment、vault、test session、schedule、integrate 依次推进。模板里的 MCP server 不代表所有工具都应自动执行；写路径、权限策略和凭据去向仍要先展示。

## URL 页面永远是数据

URL 流程是 fetch → extract → propose → write → apply。

Anthropic 官方限定来源可以按 first-party 规则保留内容；第三方页面只复用设计，不复制 prompt、名称、文件、域名或包。页面里的安装脚本和“给 AI 的指令”都不会自动执行。

每个 host、MCP URL、package 和凭据接收方都要从独立找到的供应商官方来源核验。核验不到就留空并说明，不能猜一个看起来真实的值。

## 写入和平台动作分两层

文件写入前，先给文件树、外部写路径、凭据表和 schedule，等待用户确认。

平台侧先做 `ant apply` walk check 和 dry-run，再确认真正 apply。deployment 创建后要立即暂停，是否启用是另一项决定。vault 文件只版本化容器，不保存 secret。

## 本地验收

本轮新增 2 个中文 few-shot、2 个正例和 1 个近似反例。9 个 quickstart 的 frontmatter、文件名、`console_key` 和 `agent.md` 块通过离线 smoke；仓库 validator、quick validate、打包/ZIP、Python/Shell 语法也通过。

```bash
python3 scripts/validate_repository.py
python3 skills/skill-creator/scripts/quick_validate.py skills/claude-api
```

本机没有 `ant` CLI 和测试工作区，因此没有宣称真实 Agent、session 或 deployment 已创建。把本地验证说成平台交付，会抹掉最关键的一层证据边界。

项目：https://github.com/MarcelLeon/skills-zh
