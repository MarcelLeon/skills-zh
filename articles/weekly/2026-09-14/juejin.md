---
title: Managed Agents 权限处理：别把 auto 当成人工审批门
category: 人工智能
tags: [Claude, Agent, 安全, API]
summary: 拆清 auto 的 allow、ask、deny 三种结果，并按事件而不是配置策略实现客户端。
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

# Managed Agents 权限处理：别把 auto 当成人工审批门

Anthropic Agent Skills 上游 `34040c9` 为 Managed Agents 加入 `auto` 权限策略。最重要的不是多了一个配置值，而是客户端必须改变分流方式。

## `auto` 有三条路径

- `allow`：服务端判定可执行，工具直接运行；
- `ask`：无法确定，session 暂停等待 `user.tool_confirmation`；
- `deny`：判定高风险，工具不运行，Agent 收到错误结果后 session 继续。

如果人类必须在副作用发生前逐次查看，应该使用 `always_ask`。`auto` 不是人工检查点。

## 读取 `evaluated_permission`，不要猜

`agent.tool_use` 和 `agent.mcp_tool_use` 都携带 `evaluated_permission`。客户端只对 `ask` 发确认；`deny` 分支记录 `evaluation.type` 与 `reason_code`，不能再用确认事件覆盖。确认拒绝的文本字段是 `deny_message`，`tool_use_id` 则取 `sevt_...` 事件 ID。

日志处理还要容忍未知 `evaluation.type` 或 `reason_code`，避免 API 扩展后客户端崩溃。

## 注意 `user.message` 的信任含义

应用发到 `user.message` 的文本会被评估器当作应用意图。即使内容来自终端用户，直接转发也会进入这个信任语境。工具结果、网页、MCP 响应和线程间消息不会获得相同权重。

因此对高风险工具，接入方要根据自身信任模型决定是否固定 `always_ask`。

## 交互排障的新入口

`ant beta:sessions connect <session-id>` 可以加载 transcript、跟随主线程、发消息、interrupt，并处理工具确认。`--web` 会在 `127.0.0.1` 打开本地 viewer，额外展示多 Agent 的所有线程。

脚本仍应使用 events stream/send。Ctrl+C 只断开 viewer，不终止 session。

## 本地验收

本周同步范围为 1 个提交、1 个 Skill、7 个文件、+116/-16。仓库 validator 通过 19 个中文 Skill；`claude-api` quick validate、打包/ZIP、Python/Shell 语法、14 个正例与 7 个反例的路由 smoke、6 个事实 reference 的 hash parity 均通过。

限制：本机没有 `ant` CLI 和测试 session，没有真实运行 `connect`、`--web` 或 `auto` 三路服务端判定，也没有调用 Claude API。

项目：https://github.com/MarcelLeon/skills-zh
