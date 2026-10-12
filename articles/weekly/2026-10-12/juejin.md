---
title: Managed Agents 超过 25 个子线程，如何切到 dynamic workflows
category: 人工智能
tags: [Claude, Agent, 开发工具, 工作流]
summary: 用任务规模区分 roster 与 dynamic workflows，并补齐预算、关闭方式和网络边界。
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

# Managed Agents 超过 25 个子线程，如何切到 dynamic workflows

多 Agent 并不等于不断扩大 roster。一个 session 最多 25 个 child thread；数百份文档或大量条目要分阶段处理时，roster 只能反复分批，dynamic workflows 才是对应能力。

Anthropic Agent Skills 上游 `dbd4588` 新增 dynamic workflows 和四个模板。skills-zh 本轮把规模判断、预算说明和关闭方式接入中文路由。

## 配置只是第一步

```python
multiagent={
    "type": "multiagent_20261001",
    "workflows": {"type": "enabled"},
}
```

Agent 的 system prompt 还要写明条件：例如“合同超过一批、需要抽取→核验→汇总时启动 workflow run；单个文件自己完成”。不要写成无条件“总是启动 workflow”。

开启后应告诉用户：run 会让多个 Agent 分阶段工作；每个 Agent 都消耗 token，所以 session 需要预算。用户明确不要时，使用 roster-only `coordinator`，或发送 `workflows: {"type": "disabled"}`。在 `multiagent_20261001` 上把 workflows 省略并不等于关闭，因为默认是开启。

## 不适合 dynamic workflows 的任务

客服问答、文档 Q&A、辅导解题等逐题任务，默认由一个 Agent 自检。不要为了“准确”给每个答案再加 checker、voter、auditor 或客户端第二次模型调用。只有一题本身要拆大量独立文件或来源，或者用户明确要求 checker 并接受额外成本，才扩展编排。

## 四个模板如何分阶段

- `bug-hunter`：找候选、筛选、证明；
- `explainer-video`：并行做 scene、统一审查、修一处；
- `performance-tuner`：逐函数优化、交叉攻击、重做、统一测量；
- `watchlist-scanner`：逐 ticker 扫描与逐 ticker 复核。

它们共同展示了 phase、失败隔离和最终验收，而不是只展示“多开几个 Agent”。

## 网络规则也需要更新

`limited.allowed_hosts` 现在也约束 Managed Agents 的 `web_search` / `web_fetch`。网页工具不用时应设为 `enabled: false`；需要时同时配置环境 host 与工具 domain。把 host 加进 allow-list 也会向 sandbox 开放，不能只把它当搜索过滤器。

## 本地验收

本轮新增 3 个中文 few-shot、3 个正例和 1 个近似反例，当前 `claude-api` 为 22 正例/9 反例。仓库 validator、quick validate、打包/ZIP、Python/Shell 语法和 13 个 quickstart 的结构 smoke 已通过。

```bash
python3 scripts/validate_repository.py
python3 skills/skill-creator/scripts/quick_validate.py skills/claude-api
```

没有 `ant` CLI 和测试工作区，所以没有把离线验证写成真实 workflow run 成功。Haiku 5.5 迁移 reference 也已同步，但本轮未发起真实模型调用。

项目：https://github.com/MarcelLeon/skills-zh
