---
title: Agent的auto不是人工审批
tags: [Claude, AIAgent, 安全设计, 开发工具]
images: []
---

Agent 工具权限里的 `auto`，不是“自动弹人工审批”。

Managed Agents 的 `auto` 每次可能：

1️⃣ `allow`：工具直接执行；
2️⃣ `ask`：拿不准，暂停等确认；
3️⃣ `deny`：高风险，拒绝后 Agent 继续。

所以客户端要看事件里的 `evaluated_permission`，不能按配置值猜：

✅ 只对 `ask` 发确认；
✅ `deny` 记录 `evaluation` / `reason_code`；
✅ 拒绝理由用 `deny_message`；
✅ 必须人工逐次审核的工具，固定 `always_ask`。

另一个坑：应用发进 `user.message` 的文本会被当作应用意图。若它原本来自不可信用户，不能期待 `auto` 自动补上最终人工门禁。

这周 skills-zh 也同步了 `ant beta:sessions connect`：终端接管主线程，`--web` 本地 viewer 看全部多 Agent 线程。

本地验证通过 19 个中文 Skill、打包/ZIP、语法、路由和上游 reference 一致性。边界也写清：没装 `ant` CLI，没跑真实 session，没调用 Claude API。

#Claude #AIAgent #安全设计 #开发工具
