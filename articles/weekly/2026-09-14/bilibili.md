---
title: Agent 的 auto 权限，为什么不等于人工审批
tags: [Claude, Agent, 安全, 开发工具]
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---
Agent 的 auto 权限，为什么不等于人工审批
上游版本：34040c9
本周范围：1 个提交，1 个 Skill，7 个文件
一、auto 有三种结果
Managed Agents 的 auto 会逐次评估工具调用。
allow：工具直接执行。
ask：session 暂停，等待客户端确认。
deny：高风险调用不执行，Agent 收到错误结果后继续。
所以 auto 不保证人类会在执行前看到调用。必须逐次人工复核的工具要用 always_ask。
二、客户端按事件分流
agent.tool_use 和 agent.mcp_tool_use 都有 evaluated_permission。
只对 ask 发送 user.tool_confirmation。
deny 分支记录 evaluation.type 和 reason_code，不能补确认覆盖服务端拒绝。
拒绝理由字段是 deny_message，tool_use_id 使用 sevt 开头的事件 ID。
三、user.message 是信任边界
应用发入 user.message 的内容会被评估器视为应用意图。若它来自不可信终端用户，接入方不能假设 auto 会替代最终人工检查。
工具结果、网页、MCP 响应和线程间消息不会获得相同权重。
四、交互接管 session
ant beta:sessions connect 可以加载记录、跟随主线程、发消息、interrupt，并处理工具确认。
加 --web 会在本地打开 viewer，并展示多 Agent 的全部线程。脚本仍然使用 events stream 和 send。
五、本地验证与边界
仓库 validator 通过 19 个中文 Skill。claude-api 的 quick validate、打包、ZIP、Python 和 Shell 语法、14 个正例与 7 个反例的路由 smoke、6 个事实 reference 一致性均通过。
本机没有 ant CLI 和测试 session，没有真实运行 connect、Web viewer 或 auto 三路服务端判定，也没有调用 Claude API。
项目地址：
https://github.com/MarcelLeon/skills-zh
