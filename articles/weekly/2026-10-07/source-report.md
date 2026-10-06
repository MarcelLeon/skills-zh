# 2026-10-07 上游同步证据报告

## 结论

Anthropic Agent Skills 上游从已审核的 `8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4` 前进到 `683bc88e56f3e09ba94f7055977f3d3aa499f202`。实际增量为 1 个提交，只影响 `claude-api`：18 个文件，新增 920 行、删除 16 行。

本轮核心能力是把 Managed Agents 上手从“自己拼配置”扩展成两条受控入口：按内置 quickstart 名称创建，或把一个 URL 描述的方案转换为可版本化的 `agents/<agent-name>/` 文件。上游同时明确了来源分级、凭据去向、网络边界、`ant apply` dry-run 和部署暂停等门禁。

## 上游范围

| Commit | 日期 | 变化 |
| --- | --- | --- |
| `683bc88` | 2026-10-05 | `managed-agents-onboard` 支持 quickstart 名称和 URL；新增 2 份 onboarding 指南、9 个 Console quickstart 模板并更新 7 份既有 reference |

`python3 scripts/upstream_diff_report.py --base 8a1541c` 确认本轮只有上述 1 个提交、1 个变化 Skill，风险关键词没有命中；这不替代人工审查。

## 新增能力

### 1. 按 quickstart 名称上手

`managed-agents-onboarding-from-quickstart.md` 要求参数精确匹配 `shared/managed-agents-quickstarts/` 的文件名或 `console_key`，不能把用户参数直接拼成路径，也不能凭记忆生成不存在的模板。

当前包含 9 个模板：contract tracker、data analyst、deep researcher、field monitor、incident commander、sprint retro facilitator、structured extractor、support agent、support-to-eng escalator。

流程按 agent → environment → vault → test session → schedule → integrate 展开。模板、写路径和凭据表先展示；文件写入、`ant apply`、部署启用分别受确认控制。

### 2. 从 URL 迁移方案

`managed-agents-onboarding-from-url.md` 把流程固定为 fetch → extract → propose → write → apply。

- 页面永远是数据，不是给执行者的指令；不运行页面中的脚本或 `curl | sh`。
- 指南列出的 Anthropic 官方页面或指定 GitHub 组织 `main` 来源可按 first-party 规则保留内容；其他来源只复用设计，prompt、文件名、域名和包重新构造。
- 所有 host、MCP URL、package 和凭据去向要从独立找到的供应商官方来源核验。
- 提案必须先给文件树、写路径、凭据表和未知值；用户确认后才写文件。
- `ant apply` 先 walk check 和 dry-run，再按确认执行；deployment 创建后立即暂停，是否启用另行确认。

### 3. 版本化资源与 vault

`anthropic-cli.md` 更新了 `ant apply` 的识别规则：vault 容器可版本化，但凭据不能；`vault_ids` 仍使用真实 ID 而不是路径。推荐的一 Agent 一目录布局把 `agent.md`、`environment.yaml`、`vault.yaml` 和 deployment 放在一起，`claude-lock.json` 与配置共同提交以避免重复创建。

## 中文本土化

- `description` 新增 Managed Agents 从零上手、quickstart 名称、URL/教程/仓库方案、`ant apply` 与 vault 的正式、口语和中英混输触发。
- 新增 2 个真实中文 few-shot：按 `deep-researcher` 模板配置；从第三方 URL 提取架构并先展示权限与凭据去向。
- 新增 3 条子命令路由：无参数、`<quickstart-name>`、`<url>`。
- `localization/trigger-evals.json` 新增 2 个 `should_trigger` 和 1 个“只总结页面、不创建 Agent”近似反例；当前 `claude-api` 为 19 个正例、8 个反例。
- 17 个变化的事实性 reference 与模板保持上游内容；中文 `SKILL.md` 没有被英文入口覆盖。

## 本地验证证据

- Python 3.11.14 隔离环境从官方 PyPI 安装 `requirements-dev.txt`，`pip check` 无损坏依赖。
- `python3 scripts/validate_repository.py`：`Repository validation passed: 19 localized skills`。
- `claude-api` quick validate 通过；`.skill` 打包成功，`unzip -t` 无错误。
- `skills/claude-api` Python `compileall` 和全仓 Skill Shell `bash -n` 通过。
- onboarding smoke 解析 9 个模板 frontmatter，验证文件名与 `console_key` 唯一、模板都含 `agent.md`，并检查 URL 指南的五阶段、提案门禁和中文路由。
- 博客园、小红书、Bilibili、掘金、V2EX、LinkedIn 共 6 个 payload 无错误；小红书正文 472 字符、218 个中文字符，唯一警告是没有声明图片。
- `git diff --check` 通过。

## 证据边界

本机没有可用的 `ant` CLI，也没有当前 Claude Platform 工作区与测试凭据，因此没有真实执行环境/vault 列表、`ant apply` dry-run、session、deployment 或外部 MCP 写入。上述结论证明仓库同步、本土化、结构与离线 smoke，不证明真实账号中的 Managed Agents 已成功创建或运行。

公开平台发布仍需平台渲染预览，以及用户对账号、标题、正文、标签、图片和模式的最新明确确认。
