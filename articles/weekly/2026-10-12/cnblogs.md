---
title: 25 个子线程不够时，Managed Agents 该用 dynamic workflows 了
tags: [Claude API, Managed Agents, Dynamic Workflows, Agent]
categories: [AI]
links:
  - https://github.com/MarcelLeon/skills-zh
images: []
---

# 25 个子线程不够时，Managed Agents 该用 dynamic workflows 了

多 Agent 系统有一个常见误区：任务越大，就给 roster 塞更多角色，再让 coordinator 一批批派活。这个方法在任务只有十几个独立部分时有效；面对数百份合同、几百个代码文件或大量标的扫描时，它会把编排本身变成瓶颈。

Anthropic Agent Skills 上游 `dbd4588` 为 `claude-api` 增加了 Managed Agents dynamic workflows。skills-zh 本轮同步的不只是新配置，还把“什么时候该用、什么时候不该用、怎么关闭、网络边界怎么算”接入中文任务路由。

## 一、先判断工作规模，不要看到“并行”就上 workflow

Roster 适合若干边界清楚的任务：主 Agent 委派给 `self`、便宜 worker 或专门角色，每个 subagent 都有自己的 thread 和上下文。

Dynamic workflows 处理的是另一种规模：整项工作碎片多到 session 的 25 个 child thread 不够，roster 必须分批才能跑完。例如 600 份合同先抽取条款、再交叉核验、最后汇总风险表。

反过来，客服问答、文档 Q&A、辅导解题等“一次解决一个问题”的任务不应默认给每个答案再加 checker、voter 或 auditor。它们会把每个答案的成本成倍放大。让同一个 Agent 自检，配好文档、工具和 effort，通常才是默认路径。

## 二、开启 dynamic workflows 需要两个条件

第一个条件是 Agent 配置：

```python
multiagent={
    "type": "multiagent_20261001",
    "workflows": {"type": "enabled"},
}
```

第二个条件是 system prompt 中的条件式规则。仅打开能力，不代表 Agent 知道何时应该启动 workflow run。规则需要说明：大量条目、分阶段处理时启动 run；单个文件、小修复或普通问答自己完成。

还要向用户说明两件事：run 会让多个 Agent 分阶段处理任务；每个 Agent 都消耗 token，因此 session 需要预算。用户说不要 workflows 时，不能依赖默认值继续开启；应改用 roster-only `coordinator`，或显式设置：

```python
"workflows": {"type": "disabled"}
```

## 三、四个 quickstart 展示了分阶段工作流

上游新增了四个模板：

1. `bug-hunter`：多名 reader 找候选 bug，reviewer 汇总，再由 prover 用最小测试证明；
2. `explainer-video`：按 scene 并行生成，再统一检查和修复；
3. `performance-tuner`：每个函数独立优化、交叉验证、重做弱结果，最后统一测量；
4. `watchlist-scanner`：逐 ticker 扫描，再逐 ticker 复核，失败项不能伪装成 neutral。

四个模板都使用 `multiagent_20261001`、启用 workflows，并关闭普通 subagents。这里的重点不是照抄角色，而是观察 phase、失败隔离、预算说明和最终验收如何组合。

## 四、网页工具的网络边界也变了

本轮还有一项容易漏掉的安全修复。旧 reference 认为 `web_search` / `web_fetch` 运行在 Anthropic 服务端，所以不受 environment networking 影响。上游现在明确：在 `limited` 网络下，`allowed_hosts` 同样约束这两个网页工具。

如果 `allowed_hosts` 为空，抓取拿不到页面，搜索也不返回结果。推荐默认关闭不用的网页工具；需要网页时，同时配置环境 `allowed_hosts` 和工具 `allowed_domains`/`blocked_domains`。注意：放入 `allowed_hosts` 的站点也会向 sandbox 开放。

## 五、同轮更新的 Haiku 5.5 也不是换一个 ID

Claude Haiku 5.5 现在映射为 `claude-haiku-5-5`，但从 Haiku 4.5 迁移时还要处理：

- `budget_tokens` 改为 adaptive thinking 与 effort；
- 移除非默认 sampling 参数和 assistant prefill；
- 在 Claude API 与 Google Cloud 上升级 computer toolset；
- 回放 thinking blocks 时保持历史 append-only；
- 在读取内容前处理 `stop_reason: "refusal"`；
- 按 100K 输入分界重算价格，并用新 tokenizer 重做 token 基线。

## 六、skills-zh 如何验收

中文入口新增 3 个 few-shot，触发集增加 3 个正例和 1 个 GitHub Actions matrix workflow 近似反例，当前为 22 个正例、9 个反例。

可复现的本地命令：

```bash
python3 scripts/validate_repository.py
python3 skills/skill-creator/scripts/quick_validate.py skills/claude-api
PYTHONPATH=skills/skill-creator python3 -m scripts.package_skill skills/claude-api /tmp/skill-dist
python3 -m compileall skills/claude-api
```

仓库 validator、quick validate、打包/ZIP、Python/Shell 语法和特性 smoke 已通过。52 个事实性支撑文件与上游 Git blob 一致，另有 1 个文件只做行尾空格归一化。

## 限制

本机没有 Managed Agents `ant` CLI 和测试工作区，因此没有真实启动 workflow run，也没有调用 Haiku 5.5。这里证明的是仓库同步、本土化和离线验收，不是平台运行、成本或模型质量回执。

项目地址：https://github.com/MarcelLeon/skills-zh
