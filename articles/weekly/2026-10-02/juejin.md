---
title: Claude 应用调 Prompt，先把 eval 做成可审计闭环
category: 人工智能
tags: [Claude, Agent, Prompt, 测试]
summary: 从真实样本、grader 到 train/validation/test，把 Prompt 迭代变成可复现实验。
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

# Claude 应用调 Prompt，先把 eval 做成可审计闭环

Agent 改完 Prompt 后挑几个成功案例，证明不了整体质量提升。Anthropic Agent Skills 上游 `8a1541c` 新增 build-eval、eval-audit、eval-hillclimb、cost-hillclimb 以及报告/runner 资产，skills-zh 本轮把它们接入中文 `claude-api` 路由。

## 可信 eval 的三个组成

一套可用评测至少需要：代表真实工作的输入、复用生产路径的 runner、能判断目标质量的 grader。

输入可以来自脱敏生产记录、已有测试或针对边界合成的案例，但必须让使用者确认“这些确实是我关心的问题”。grader 也要先确认，避免把格式整齐误当成业务正确。

真实 Claude API 运行会产生费用。先跑小样本测出单次成本，再确认全量预算，而不是执行后才补账。

## audit 在 hillclimb 前

`eval-audit.md` 检查 case、harness、metrics 与 grader：测试是否走了真实工具链，指标是否掩盖严重失败，grader 是否看到不该看到的答案，以及这套 eval 能否区分准备比较的改动。

通过审计后，`eval-hillclimb.md` 才进入 train/validation/test 循环：

1. train 找模式和失败原因；
2. validation 选择候选改动；
3. test 保持独立，作为最终判断；
4. 每轮记录 diff、分数、token/费用和停止条件。

上游提供轻量 HTML report builder 与 runner scaffold，不需要临时再写一套不可比较的结果页。

## 模型迁移也进入同一条证据链

上游示例默认更新为 Claude Opus 5.5，并加入 Claude Sonnet 5.5。迁移不能只替换 model id，还要检查 thinking/effort、forced tool use、平台可用性和 preserved-thinking 历史前缀。

对于 streaming client tools，`eager_input_streaming: true` 能让大参数边生成边到达，但客户端必须在执行工具前解析并按 schema 校验；遇到截断或 refusal 时不能执行副作用。

## 本地验收入口

```bash
python3 scripts/validate_repository.py
python3 skills/skill-creator/scripts/quick_validate.py skills/claude-api
```

本轮同步范围：2 个提交、1 个 Skill、72 个上游文件、+6982/-620。19 个 Skill 的仓库 validator、`claude-api` quick validate/打包、Python/Shell/Node 语法、17 正例/7 反例路由、事实内容 parity（另有 16 处纯空白归一化）、诊断脚本 dry-run、报告构建 smoke 与六平台 payload 均通过。

限制：未获得付费运行预算确认，因此没有调用真实 Claude API，也没有跑全量 eval、hillclimb 或 preserved-thinking replay。

项目：https://github.com/MarcelLeon/skills-zh
