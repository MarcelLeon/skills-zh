---
title: 25个子线程不够怎么办
tags: [Claude, AIAgent, 多Agent, 开发工具]
images: []
---

多 Agent 不是越多越好。一个 Managed Agents session 最多 25 个 child thread；几百份合同、文件或标的要分阶段处理时，硬塞 roster 只会不断分批。

这周 skills-zh 同步了 dynamic workflows：

1️⃣ 大任务用 `multiagent_20261001`，让 workflow run 分阶段调度；
2️⃣ system prompt 要写清什么时候启动，不能无条件“总是用 workflow”；
3️⃣ 每个 Agent 都消耗 token，要给 session 预算并告诉用户；
4️⃣ 用户说不要时，改用 coordinator roster 或显式关闭；
5️⃣ 客服问答、文档 Q&A 这类单问单答，默认一个 Agent 自检，不堆 checker/voter。

同时修正一个安全边界：`limited.allowed_hosts` 现在也限制 `web_search` 和 `web_fetch`。不用网页就关掉，需要时同时限制环境 host 和工具 domain。

本轮还同步 Haiku 5.5 迁移清单。不是只换模型 ID，还要处理 thinking、sampling、prefill、computer tool 和历史回放。

已通过仓库 validator、打包、ZIP、语法和 13 个 quickstart 结构检查；没有真实跑平台 workflow 或模型调用。

#Claude #AIAgent #多Agent #开发工具
