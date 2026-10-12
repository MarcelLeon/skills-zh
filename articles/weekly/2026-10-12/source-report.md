# 2026-10-12 上游同步证据报告

## 结论

Anthropic Agent Skills 上游从已审核的 `683bc88e56f3e09ba94f7055977f3d3aa499f202` 前进到 `dbd4588f9e1033efb41dad4bef2f7947c8993d44`。实际增量为 2 个提交，只影响 `claude-api`：54 个文件，新增 1812 行、删除 413 行。

本轮有三类实质变化：Claude Haiku 5.5 成为当前 Haiku；Managed Agents 新增处理大规模分阶段任务的 dynamic workflows 和 4 个 workflow quickstart；`limited.allowed_hosts` 现在也约束服务端 `web_search` / `web_fetch`，纠正了旧 reference 中“环境网络不影响网页工具”的结论。

## 上游范围

| Commit | 日期 | 变化 |
| --- | --- | --- |
| `9d63080` | 2026-10-09 | Claude Haiku 5.5、Managed Agents 与 preserved-thinking 修复 |
| `dbd4588` | 2026-10-09 | Dynamic workflows、4 个 workflow quickstart、网页工具网络规则 |

`python3 scripts/upstream_diff_report.py` 在同步前确认 2 个提交、1 个变化 Skill；风险关键词没有命中，但本轮仍人工审阅了模型迁移、网络边界、工作流规模判断和新增模板。

## 上游核心变化

### 1. Dynamic workflows 不是更大的 roster

Roster 适合若干可独立委派的任务；每个 session 最多 25 个 child thread。整项工作有数百个条目、roster 必须分批才能完成时，dynamic workflows 更合适：服务端按阶段执行 workflow run，run 的线程不占这 25 个 child thread 名额。

开启配置是 `multiagent: {"type": "multiagent_20261001", "workflows": {"type": "enabled"}}`。只设置开关不够，还要在 Agent 的 system prompt 中写明哪些规模的任务启动 run、哪些小任务自己完成。每个 run 中的 Agent 都消耗 token，因此要告诉用户并配置 session 预算。用户明确不要 workflows 时，应使用 roster-only `coordinator`，或显式设置 `workflows: {"type": "disabled"}`。

本轮新增 4 个动态工作流模板：`bug-hunter`、`explainer-video`、`performance-tuner`、`watchlist-scanner`。它们都使用 `multiagent_20261001`，启用 workflows，并关闭普通 subagents。

### 2. 单问单答不能默认堆复核 Agent

上游新增了明确反例：客服问答、文档 Q&A、辅导解题等逐题任务，默认由同一个 Agent 自检，不应为了“更准确”给每个答案再加 checker、voter、auditor 或客户端第二次模型调用。只有一题本身要拆大量独立来源/文件，或用户明确要求 checker 并接受额外成本时，才扩大编排。

### 3. `allowed_hosts` 也约束网页工具

旧 reference 认为 Managed Agents 的 `web_search` / `web_fetch` 运行在服务端，所以不受 environment networking 影响；本轮上游把结论改为：`limited.allowed_hosts` 同样生效。没有 host 时，网页抓取拿不到页面，网页搜索也不返回结果。

这带来一个重要配置边界：不需要网页时，将两个工具设为 `enabled: false`；需要时，环境 `allowed_hosts` 与工具 `allowed_domains`/`blocked_domains` 共同收紧。加入 `allowed_hosts` 的站点也向 sandbox 开放，不能只把它理解成搜索结果过滤器。

### 4. Haiku 5.5 不是模型 ID 替换

Claude Haiku 5.5 使用 `claude-haiku-5-5`，1M context、128K max output，并成为用户只说“Haiku”时的当前映射。Haiku 4.5 代码迁移还要处理 adaptive thinking/effort、移除 `budget_tokens` 与非默认 sampling 参数、去掉 assistant prefill、升级 computer toolset、保持 replay 历史 append-only、优先处理 `stop_reason: "refusal"`，并按 100K 输入分界重算价格和 token 基线。

## 中文本土化

- `description` 补充 Haiku 5.5、dynamic workflows/workflow run 等正式表达和中英混输触发，压缩后为 758 字符。
- 新增 3 个真实中文 few-shot：600 份合同的分阶段 workflow；Haiku 4.5 到 5.5 迁移；`docs.example.cn` 受限网络与网页工具收紧。
- 新增单问单答不过度编排、workflow 关闭方式、Messages API 大任务只提示一次 Managed Agents 方案等边界。
- `localization/trigger-evals.json` 新增 3 个 `should_trigger` 与 1 个 GitHub Actions matrix workflow 近似反例；`claude-api` 现有 22 个正例、9 个反例。
- README、marketplace、UPSTREAM_SYNC 和同步基线更新到 `dbd4588`；marketplace 版本为 `1.0.7`。
- 52 个变化的事实性支撑文件与 `upstream/main` Git blob 完全一致；`cost-hillclimb.md` 仅清理 4 处上游行尾空格；中文 `SKILL.md` 未被英文入口覆盖。

## 本地验证证据

- Python 3.11.14 隔离环境从官方 PyPI 安装 `requirements-dev.txt`，`pip check` 无损坏依赖。
- `python3 scripts/validate_repository.py`：`Repository validation passed: 19 localized skills`。
- `claude-api` quick validate 通过；`.skill` 打包成功，`unzip -t` 无错误。
- `skills/claude-api` Python `compileall` 通过；全仓 2 个 Skill Shell 脚本通过 `bash -n`。
- 特性 smoke 解析 13 个 quickstart，确认 4 个新模板的 `console_key` 唯一、dynamic workflows 开启、普通 subagents 关闭。
- 特性 smoke 同时检查 25 child thread 边界、预算告知、关闭方法、条件式 system prompt、Haiku 5.5 迁移清单和 `limited.allowed_hosts` 新规则。
- 博客园、小红书、Bilibili、掘金、V2EX、LinkedIn 共 6 个 payload 无错误；小红书正文 669 字符、207 个中文字符，唯一警告是未声明图片。
- `git diff --check` 通过。

## 证据边界

本机没有 Managed Agents 的 `ant` CLI，也没有当前 Claude Platform 测试工作区与凭据；本轮未真实启动 workflow run、调用 Claude Haiku 5.5、创建 Agent/session/deployment 或执行外部工具写入。本地证据证明同步、本土化、结构、打包和离线规则检查，不证明真实平台运行结果、成本或模型质量。

公开平台发布仍需平台渲染预览，以及用户对账号、标题、正文、标签、图片和模式的最新明确确认。
