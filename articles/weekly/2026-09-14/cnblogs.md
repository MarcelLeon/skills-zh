---
title: Managed Agents 的 auto 权限，不是“自动人工审批”
tags: [Claude API, Managed Agents, Agent, 安全]
categories: [AI]
links:
  - https://github.com/MarcelLeon/skills-zh
images: []
---

# Managed Agents 的 auto 权限，不是“自动人工审批”

给 Agent 加权限控制时，一个很容易犯的错是看到 `auto`，就把它理解成“自动判断是否弹出人工确认”。

Anthropic Agent Skills 上游 `34040c9` 补齐了 Managed Agents 的真实语义：`auto` 每次会产生三种结果——直接运行、直接拒绝、暂停等待确认。它并不保证人类会在工具执行前看到调用。

skills-zh 本周把这组事实接入中文 `claude-api` 路由，并把客户端应该如何消费事件、如何留审计记录、何时必须退回 `always_ask` 写成了中文场景。

## 一、三种策略不是三个风险等级

`always_allow` 会自动执行；`always_ask` 会让 session 以 `requires_action` 暂停，等待客户端发 `user.tool_confirmation`。

`auto` 则由服务端评估本次调用，结果是：

1. `allow`：工具直接运行；
2. `ask`：无法确定时暂停，等待人工允许或拒绝；
3. `deny`：高风险调用不运行，Agent 收到错误 tool result，session 继续。

所以“必须由人审批”的工具不能配置成 `auto`。如果操作的副作用不可逆，或组织流程要求逐次复核，应明确使用 `always_ask`。

## 二、客户端按事件结果分流

旧实现很可能按配置策略判断：

```text
如果 policy 是 always_ask，就发送确认
```

这在 `auto` 加入后不够。正确的分流依据是 `agent.tool_use` 或 `agent.mcp_tool_use` 事件上的 `evaluated_permission`：

```text
allow -> 已执行，记录结果
ask  -> 发送 user.tool_confirmation
deny -> 记录 evaluation，等待 Agent 继续
```

确认事件里的 `tool_use_id` 是事件 ID，通常以 `sevt_` 开头，不是模型侧的 `toolu_` ID。拒绝理由字段使用 `deny_message`；向非 `ask` 事件补确认会返回 400。

审计日志至少应保留 `evaluated_permission`、`evaluation.type` 和已知的 `reason_code`。客户端还要容忍未来出现的新枚举：对认识的值分支，对未知值记录并透传。

## 三、`user.message` 是一条容易忽略的信任边界

权限评估会把应用发出的 `user.message` 当作应用意图。若应用只是把不可信终端用户文本原样转发，评估器仍会在这个上下文里判断工具调用。

来自工具结果、网页、MCP 响应或线程间消息的同样文字，不具备相同权重。

这不是说 `auto` 不安全，而是说明接入方不能把“输入来自哪里”藏在统一的 `user.message` 里，再把 `auto` 当最终的人类检查点。真正需要人审的工具，仍要固定成 `always_ask`。

## 四、用 `ant beta:sessions connect` 接管现场

上游还新增了交互式 session viewer：

```bash
ant beta:sessions connect <session-id>
ant beta:sessions connect <session-id> --web
```

终端模式会加载 transcript、持续跟随主线程，并允许发送消息、interrupt 或处理等待中的工具确认。Ctrl+C 只是断开，session 不会因此终止。

`--web` 在本机 `127.0.0.1` 启动 viewer，能看到多 Agent 的所有线程；终端只跟随主线程。Web URL 需要在两分钟内首次打开，浏览器通过本地 `ant` 进程访问 API，凭据不离开 CLI。

非交互程序仍应使用 events stream/send，不能拿 viewer 代替稳定的自动化接口。

## 五、如何复现本地验收

仓库级校验：

```bash
python3 scripts/validate_repository.py
```

本轮结果为 `Repository validation passed: 19 localized skills`。`claude-api` 还通过 quick validate、Python/Shell 语法、分发包与 ZIP 完整性、中文路由 smoke，以及 6 个变化 reference 的 Git blob 一致性检查。

## 限制

本周实际范围是 `41bbe19..34040c9`：1 个提交、1 个 Skill、7 个文件、+116/-16。

本机没有安装 `ant` CLI，也没有可用测试 session，因此没有运行真实 `connect` / `--web`，没有触发 `auto` 的 allow、ask、deny 三条线上分支，也没有验证确认错误的 400 响应。本文证明的是上游事实同步与本地确定性验收，不是 Managed Agents 生产环境端到端结果。

项目地址：https://github.com/MarcelLeon/skills-zh
