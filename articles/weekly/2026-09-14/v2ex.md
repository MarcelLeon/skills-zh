---
title: Agent 工具权限的 auto，你会把它当成人工审批门吗？
node: programmer
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

最近同步 Anthropic Agent Skills 的 `claude-api`，上游新增了 Managed Agents 的 `auto` 权限策略。最值得讨论的一点是：`auto` 不是“所有调用先自动评估，再弹给人确认”。

它有三种结果：

1. `allow`：服务端判断安全，工具直接执行；
2. `ask`：无法确定，session 暂停等待客户端确认；
3. `deny`：判定高风险，工具不执行，Agent 收到错误结果后继续。

所以客户端不应该按配置的 policy 分支，而要看每个 `agent.tool_use` / `agent.mcp_tool_use` 的 `evaluated_permission`。只对 `ask` 发 `user.tool_confirmation`；`deny` 要记审计字段，但不能再补确认。拒绝理由字段是 `deny_message`，不是 `message`。

另一个边界是 `user.message`。应用发进去的文本会被权限评估器视为应用意图；如果只是把终端用户输入原样中转，这个来源差异不会自动保留。真正要求人工逐次复核的工具，还是应该配置 `always_ask`。

上游还补了 `ant beta:sessions connect`：终端能跟随主线程、发消息、interrupt、允许或拒绝等待中的工具；`--web` 本地 viewer 可以看多 Agent 的全部线程。脚本仍然走 events stream/send。

本地确定性验证已过：19 个 Skill 的仓库 validator、`claude-api` 打包/ZIP、Python/Shell 语法、路由 smoke 和 6 个事实 reference 的 hash parity。没有 `ant` CLI 和测试 session，所以没有实际跑 `connect`，也没有触发服务端三种判定。

你们做 Agent 工具权限时，会按“工具名”固定策略，还是根据参数和会话上下文动态判断？对于不可逆操作，`auto` 与 `always_ask` 的边界怎么定？

项目：https://github.com/MarcelLeon/skills-zh
