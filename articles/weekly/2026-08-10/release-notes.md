# skills-zh 2026.08.10 产品发布说明

## 发布信息

| 项目 | 内容 |
| --- | --- |
| 发布主题 | Managed Agents 生产治理能力更新 |
| 发布日期 | 2026-08-10 |
| 上游版本 | Anthropic skills `f17010c` |
| 影响范围 | `claude-api`，18 个上游文件 |
| 中文版本 | `codex/weekly-skills-zh-2026-08-10` / `78f72d5` 之后的发布补充提交 |
| 交付状态 | Draft PR #1，远端 `validate` CI 已通过 |

## 发布摘要

本次更新将 Managed Agents 从“功能参考”推进到更完整的生产治理说明，重点覆盖成本上限、数据驻留、仓库指令信任边界、Advisor 与多 Agent 分工。

skills-zh 继续采用“事实 reference 对齐上游、中文入口按真实任务重构”的维护方式：17 个变化 reference 保持与 Anthropic 上游一致，中文 `SKILL.md` 负责自然触发、任务路由、few-shot 和近似反例，不制造第二套 API 事实。

## 核心能力

### 1. 成本治理：Session 与 Deployment 预算

- Session budget 是按公开价计算的美元硬上限，不是 Messages API 的 token 型 `task_budget`。
- 达到上限后，Session 以 `budget_reached` 暂停；历史和 sandbox 保留。
- 普通消息不能恢复暂停状态，必须修改或移除预算。
- Session budget 只能创建时加入，移除后不能重新加入。
- Deployment budget 可以更新、清除和再次加入，并复制到后续触发的 Session。

### 2. 合规治理：Inference Geo

- Managed Agents 将 `inference_geo` 设置在 `model` 对象中，而不是 Messages API 的请求顶层。
- Coordinator、Worker 和 Advisor 的 geo 必须全部一致，或全部不设置。
- Workspace 允许区域后续收紧时，既有 pin 不会自动获得豁免。

### 3. 指令治理：Repository Skills

- Cloud sandbox 在 Session 启动时发现仓库根目录 `.claude/skills/<skill-name>/`。
- 只扫描根目录下一层，并且每个 Session 只扫描一次。
- 仓库写权限同时成为 Agent 指令权限；外部 PR 和贡献者内容应在挂载前审计。

### 4. 协作治理：Advisor 与 Multiagent

- 多 Agent 先从 `self` 验证分工价值，再把搜索、阅读、抽取交给低成本 Worker。
- 只有工具和职责确实不同，才增加 Reviewer、Test Writer 等 Specialist。
- Managed Agents Advisor 使用专用 roster 入口，建议通过 thread events 交付。
- Managed Agents Advisor 与 Messages API Advisor tool 的参数和结果结构不能混用。

## 中文本土化

- 新增 3 个真实中文 few-shot：25 美元代码审查预算、US inference + Advisor、仓库 Skills 信任边界。
- `claude-api` 触发评测扩展为 6 个 `should_trigger` 和 3 个相邻 `should_not_trigger`。
- 近似反例覆盖普通云预算、OpenAI Responses API、LangGraph + Gemini 多 Agent，避免只因“预算”“Agent”等关键词误触发。
- Marketplace、README、上游同步文档和基线统一更新到 `f17010c`。

## 行为纠错

- Agent version 明确为顺序整数。
- Files API 上传补充 `purpose`。
- `vault_ids` 明确为 Session create-only。
- Deployment 增加 update 能力。
- Refusal category 按开放集合处理。
- Sonnet 5 加入 prefill 已移除范围。

## 验证证据

- Python 3.11 隔离环境安装 `requirements-dev.txt`：通过。
- 仓库 validator：`Repository validation passed: 17 localized skills`。
- `claude-api` quick validate、打包与 ZIP 完整性：通过。
- Python compileall 与全仓 Shell `bash -n`：通过。
- 17 个事实性 reference 与 `upstream/main` 一致性：通过。
- 六个平台文章 payload：通过。
- Draft PR #1 远端 `Validate localized skills`：成功。

## 已知限制

本次未调用真实 Managed Agents beta API，没有在当前 Anthropic 账号创建 Session 并跑到 `budget_reached`，也没有在线验证 geo pin 或 Advisor 事件。因此这些运行态行为仍标记为“上游 reference 已同步、当前账号未实测”，不对外宣称为线上验证结论。

## 升级建议

1. 使用 Managed Agents budget 前，先区分 Session、Deployment 与 Messages API `task_budget`。
2. 有数据驻留要求时，检查整个 multiagent roster，而不是只检查 Coordinator。
3. 挂载包含 `.claude/skills` 的外部仓库前，将该目录纳入代码审查和供应链审计。
4. 从最小 `self` roster 开始，基于真实任务证据增加 Worker 与 Specialist。

项目地址：https://github.com/MarcelLeon/skills-zh
