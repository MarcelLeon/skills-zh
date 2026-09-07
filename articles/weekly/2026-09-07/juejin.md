---
title: Claude API 成本优化：先做 token profile，再决定要不要换模型
category: 人工智能
tags: [Claude, Agent, 成本优化, API]
summary: 把 Claude API 降本拆成基线、free wins、质量取舍和逐项验证，而不是直接换便宜模型。
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

# Claude API 成本优化：先做 token profile，再决定要不要换模型

当 LLM 账单上涨时，“换个便宜模型”往往是最先想到的动作。但如果不知道 token 花在稳定前缀、用户输入、工具结果、长循环还是输出上，换模型只是把多个变量绑在一起。

skills-zh 本周对齐 Anthropic Agent Skills `41bbe19`，为中文 `claude-api` 入口加入 `cost-optimize` 路由。

## 先确定证据层级

成本画像按三层数据工作：

- 有 Admin API key：读取 Usage/Cost 报表，用真实用量和金额建立基线；
- 应用保存了 `response.usage`：按任务汇总 input、cache write、cache read 与 output；
- 两者都没有：从请求构造、上下文大小和 Agent 轮数估算，并明确不确定性。

“按任务汇总”很关键。便宜请求如果需要更多轮、更多重试或更多人工复核，不一定更便宜。

## free wins 先于 tradeoff

工作流先看 Prompt Caching、按需加载参考资料、工具结果裁剪、输出形状和 Batch。它们主要消除重复付费。

降低 effort、收紧预算、切模型和多模型路由放在后面，因为它们直接改变质量。每个 lever 单独成 diff，使用同一批冻结请求和同一判断方法测量。任何真实模型评测都会产生费用，所以先给出样本、配置和预算，再取得确认。

## Admin API 不是 Messages API

同一批上游变化新增 `shared/admin-api.md`，覆盖组织成员、workspace、API key、rate limit、服务账号、WIF 和 CMEK。普通模型 key、Admin API key 与 `org:admin` OAuth 的权限不同；服务账号和 WIF 等 OAuth-only 端点不能用 admin key 代替。

中文 few-shot 要求先给最小权限和 dry-run/只读方案，再执行明确获批的组织写操作。

## Fable 5.1 不能只换模型 ID

迁移路由新增 forced tool use、append-only history、thinking block 回放、`stop_reason: refusal`、fallback、数据保留和平台支持矩阵检查。模型与 beta 能力变化快，具体事实继续从上游 reference、Models API 或官方实时来源读取。

## 反模板设计也加入本土化验收

`frontend-design` 新增 SaaS 卡片套件、全大写眉题、单词变色、散落入场动效等检查项，并补充投研看板、中文品牌故事两个场景。规则不禁止任何风格，而是要求每个选择能说明它如何服务真实主题和用户任务。

本轮同步覆盖 2 个提交、2 个 Skill、70 个文件。仓库 validator 通过 19 个本土化 Skill；两个 Skill 的 quick validate、打包、ZIP 完整性、Python/Shell 语法、路由 smoke 与事实文件一致性均通过。

限制也要说清：没有调用真实 Claude API，没有读取真实账单，没有执行 Admin API 写操作，也没有跑模型触发 A/B。

项目：https://github.com/MarcelLeon/skills-zh
