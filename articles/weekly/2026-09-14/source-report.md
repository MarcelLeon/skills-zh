# 2026-09-14 上游同步证据报告

## 结论

Anthropic Agent Skills 上游从已审核的 `41bbe19d1a1a7eaab5e7bb9050a417e5c6cffc8f` 前进到 `34040c9c568585f6929bedeaad110ad08f079624`。本周新增 1 个提交，只影响 `claude-api`，共 7 个文件、116 行新增、16 行删除。

实质变化有两组：

1. Managed Agents 新增 `auto` 权限策略。服务端会逐次把工具调用评估为 `allow`、`ask` 或 `deny`；它不是“所有调用都等人工批准”的模式。
2. `ant beta:sessions connect` 可以把终端接到已有 session，也可用 `--web` 打开本地 viewer。终端只跟随主线程，Web viewer 可观察多 Agent 的全部线程。

本次同步还修正拒绝确认字段为 `deny_message`，并补齐 `evaluated_permission`、`evaluation` 与 `reason_code` 的事件审计语义。

## 上游范围

| Commit | 日期 | 变化 |
| --- | --- | --- |
| `34040c9` | 2026-09-10 | 更新 `claude-api` 的 Managed Agents `auto` 权限策略、事件处理与 `ant beta:sessions connect`；7 个文件，+116/-16 |

`scripts/upstream_diff_report.py` 在继承上周已审核分支后确认实际范围为 `41bbe19..34040c9`，1 个提交、1 个 Skill。主工作区仍保持在用户原有 `main`，所有写入位于独立 worktree 与分支 `codex/weekly-skills-zh-2026-09-14`。

## `auto` 的三种结果

`always_allow` 自动执行，`always_ask` 一律暂停等待 `user.tool_confirmation`。`auto` 则把每次调用的工具、输入和截至当时的 session 内容交给服务端评估：

- `allow`：工具直接执行，客户端不会先收到人工审批机会。
- `ask`：session 以 `requires_action` 暂停，客户端发送允许或拒绝确认。
- `deny`：高风险调用不执行，Agent 收到错误 tool result 后 session 继续；客户端不能再用确认事件覆盖这次拒绝。

因此客户端不能按“配置的是 `auto` 还是 `always_ask`”猜当前动作，而应读取每个 `agent.tool_use` / `agent.mcp_tool_use` 的 `evaluated_permission`。只对 `ask` 发确认；对 `deny` 记录 `evaluation.type` 和 `reason_code`，并容忍未来新增的未知枚举。

## 安全边界

上游 reference 明确：应用通过 `user.message` 发入 session 的文本会被权限评估器视为应用意图，即使它原本来自不可信终端用户；工具结果、网页内容、MCP 响应和线程间消息不具备同样权重。

这意味着 `auto` 不能替代必须由人逐次把关的控制点。若某类工具在任何情况下都需要人工复核，应对该工具使用 `always_ask`，而不是期待 `auto` 总会暂停。

拒绝确认的实际字段是 `deny_message`，不是旧示例里的 `message`。向 `evaluated_permission != "ask"` 的事件发送 `user.tool_confirmation` 会得到 400。

## 交互接管

`ant beta:sessions connect <session-id>` 会加载历史记录并继续跟随 session。终端可发消息、interrupt、允许或拒绝等待中的工具调用；Ctrl+C 只断开 viewer，session 继续运行。

`--web` 在 `127.0.0.1` 启动本地 viewer，首次打开 URL 的窗口为两分钟；页面通过本地 `ant` 进程调用 API，凭据不进入浏览器。非交互脚本仍应使用 events stream/send，而不是把交互 viewer 当自动化接口。

## 中文本土化验收

- `description` 新增“权限策略、工具审批、`auto`、`evaluated_permission` / `evaluation`、`ant beta:sessions connect`”等正式、口语与中英混输触发。
- 新增 2 个真实中文 few-shot：值班系统的 `auto` 三路事件处理，以及终端/Web viewer 接管线上 session。
- 新增 Claude Code 本地 `acceptEdits` 权限配置近似反例，避免把客户端权限模式误路由成 Managed Agents API。
- `localization/trigger-evals.json` 中 `claude-api` 当前为 14 个 `should_trigger`、7 个 `should_not_trigger`。
- 6 个变化的事实性 reference 与 `upstream/main` Git blob 完全一致；中文 `SKILL.md` 没有被英文入口覆盖。

## 验证证据

- Python 3.11.14 隔离环境安装 `requirements-dev.txt`，`pip check` 无损坏依赖。
- `python3 scripts/validate_repository.py`：`Repository validation passed: 19 localized skills`。
- `claude-api` 的 quick validate 通过。
- 全仓 Python `compileall` 与所有 Skill Shell 的 `bash -n` 通过。
- `claude-api.skill` 打包成功，`unzip -t` 无错误。
- 中文路由 smoke 通过：14 个正例、7 个反例，并命中 `auto`、`reason_code`、`sessions connect --web` 和 `acceptEdits` 近似反例。
- 上游 6 个事实性 reference hash parity 与 `git diff --check` 通过。
- 6 个平台 payload 通过 `prepare_article_pack.py` 校验且无错误；小红书正文 584 字符、193 个中文字符，唯一警告是未声明图片。

## 分支关系与限制

新分支从 `origin/main` 创建，先重放尚未合入的 2026-08-24 与 2026-09-07 两轮已验证提交，再叠加本周同步。它替代旧的两个待合入分支，不能把这些分支分别合入，否则会重复提交等价补丁。

本机没有安装 `ant` CLI，也没有可用的测试 session，因此未实际运行 `ant beta:sessions connect`、`--web` viewer、`auto` 三种服务端判定或 400 错误分支；也没有调用真实 Claude API 或执行任何工具。通过的是本地文档、路由、语法、分发包和上游事实一致性验收，不是 Managed Agents 线上端到端证明。
