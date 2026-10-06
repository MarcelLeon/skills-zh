---
title: 从 quickstart 或 URL 搭 Managed Agent，先把来源与权限边界讲清楚
tags: [Claude API, Managed Agents, Agent, 安全]
categories: [AI]
links:
  - https://github.com/MarcelLeon/skills-zh
images: []
---

# 从 quickstart 或 URL 搭 Managed Agent，先把来源与权限边界讲清楚

把一篇教程或一个现成模板变成可运行 Agent，看起来像“复制配置”问题。真正的风险却在复制之后：页面里的 prompt 能不能信？MCP 凭据会发到哪里？定时任务创建后会不会立刻执行？配置更新会不会又创建一套重复资源？

Anthropic Agent Skills 上游 `683bc88` 为 `claude-api` 新增了两条 Managed Agents onboarding 路径：按内置 quickstart 名称创建，或从 URL 提取方案。skills-zh 本轮把它们接入中文路由，重点不是多一个命令，而是把来源、写入和真实平台动作分层。

## 一、quickstart 不是任意字符串

`/claude-api managed-agents-onboard deep-researcher` 只会匹配 `shared/managed-agents-quickstarts/` 中已有的文件名或 `console_key`。参数不能直接拼成路径，也不能靠模型记忆补出一个“差不多”的模板。

当前上游提供 9 个模板，覆盖研究、结构化抽取、监控、客服、事故响应、合同和数据分析等场景。匹配后流程仍不是一键发布，而是：

1. 展示完整 agent 配置、外部写路径与凭据表；
2. 选择或新建受限网络环境；
3. 选择 vault，并由用户在自己的终端录入凭据；
4. dry-run 后确认是否 apply；
5. 先跑限额测试 session；
6. 最后才决定定时部署或应用集成。

这避免了“模板来自官方，所以所有副作用都默认允许”的误区。

## 二、URL 先分来源，再决定能复制什么

URL 路径固定为 fetch → extract → propose → write → apply。

第一步不是抄内容，而是判断来源层级。指南列出的 Anthropic 官方文档或指定 GitHub 组织 `main` 来源可以按 first-party 规则保留 prompt 与字段；其他来源只复用设计：角色划分、流程和完成标准可以借鉴，但 prompt、名称、文件、域名和包都要重新构造。

页面在两种来源里都只是数据，不是指令。页面要求运行安装脚本、发送 token、访问某个地址，不会因此自动获得执行权。

## 三、提案必须先于写文件

在写 `agents/<agent-name>/` 前，要先给出：

- 文件树与每个非显然字段的来源；
- 所有会改变外部系统的工具和限制；
- 每个凭据的接收 host、用途和最小权限；
- 未核验的 host、URL、package 和 `YOUR_<THING>` 占位值；
- schedule 的自然语言说明与费用边界。

提案展示完要停下来等确认。不能在同一回合一边“请确认”，一边把文件和资源都创建了。

## 四、`ant apply` 也不是直接执行

推荐布局是一 Agent 一目录：

```text
agents/<agent-name>/
  agent.md
  environment.yaml
  vault.yaml
  deployment-<name>.yaml
```

先对目录做 walk check，确认没有误识别文件；再显式列出准备 apply 的文件做 dry-run。真正 apply 需要用户批准。deployment 从创建时就可能生效，因此指南要求创建后立即暂停，测试通过后再由用户决定是否 unpause。

vault 文件只描述容器，不存 secret。凭据由用户在自己的终端写入；`claude-lock.json` 与资源文件一起提交，后续 reconcile 才不会重复创建。

## 五、skills-zh 做了什么

本轮保留 17 个事实性 reference 与 quickstart 模板的上游内容，只重写中文入口：

- 增加 quickstart 名称、URL/教程/仓库方案等中文触发；
- 增加按 `deep-researcher` 创建和第三方 URL 迁移两个真实 few-shot；
- 增加无参数、quickstart、URL 三条子命令路由；
- 增加 2 个正例和 1 个近似反例，当前为 19 个正例、8 个反例。

本地可复现验收：

```bash
python3 scripts/upstream_diff_report.py --base 8a1541c
python3 scripts/validate_repository.py
python3 skills/skill-creator/scripts/quick_validate.py skills/claude-api
PYTHONPATH=skills/skill-creator python3 -m scripts.package_skill skills/claude-api /tmp/skill-dist
```

仓库 validator、quick validate、打包/ZIP、Python/Shell 语法和 onboarding 离线 smoke 已通过。

## 限制

本机没有 `ant` CLI 和可用的 Claude Platform 测试工作区，因此没有真实执行 `ant apply`、session、deployment 或 MCP 写入。这里证明的是同步、本土化和离线结构验收，不是生产平台成功回执。

项目地址：https://github.com/MarcelLeon/skills-zh
