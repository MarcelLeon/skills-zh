---
title: 多 Agent 任务超过 25 个子线程后，你们会切 workflow 还是自己分批？
node: programmer
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

这周同步 Anthropic Agent Skills 的 `claude-api`，上游新增了 Managed Agents dynamic workflows。

我觉得值得讨论的不是“又多一种编排”，而是它给了一个比较具体的规模判断：一个 session 最多 25 个 child thread；如果整项工作有数百个碎片，roster 必须分批才能完成，就用 dynamic workflows 让服务端按 phase 跑 workflow run。

配置本身很短：`multiagent_20261001` 加 `workflows: enabled`。但上游要求 system prompt 也写清什么时候启动 run，不能无条件“总是用 workflow”。同时要告诉用户每个 Agent 都消耗 token，session 需要预算，并给出关闭方法。用户说不要时，用 roster-only `coordinator` 或显式 disabled。

另一个边界也挺重要：客服问答、文档 Q&A、辅导解题等一次解决一个问题的场景，不应该为了“更准确”默认加 checker、voter 或第二次模型调用。只有一题本身要拆大量文件/来源，或者用户明确要求 checker 并接受成本，才扩展编排。

这轮还有一个安全结论翻转：`limited.allowed_hosts` 现在也约束服务端 `web_search` / `web_fetch`。网页工具不用时应直接关掉；需要时既要配 environment host，也要配工具 domain。把 host 加到环境 allow-list 也意味着 sandbox 能访问它。

skills-zh 新增了 3 个中文 few-shot 和 3 正/1 反触发例，离线检查了 13 个 quickstart、4 个新 dynamic 模板、Haiku 5.5 迁移清单和网络规则。validator、打包、ZIP 和语法检查通过。

限制是本机没有 `ant` CLI 和测试工作区，没有真的跑 workflow run 或 Haiku 5.5。

大家在生产里怎么判断从 roster 切到 workflow 的阈值？你们会用“条目数/线程数”，还是按 phase、成本预算、失败恢复来判？

项目：https://github.com/MarcelLeon/skills-zh
