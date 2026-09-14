# 2026-09-14 发布计划

## 当前状态

本地文章包已生成。博客园、小红书、Bilibili、掘金、V2EX 与 LinkedIn 共 6 个 payload 已通过 `prepare_article_pack.py` 且无错误；小红书正文 584 字符、193 个中文字符，唯一警告是未声明图片。

没有打开任何平台编辑器，没有创建或覆盖远程草稿，也没有执行公开发布。

## 内容主轴

主角是 Managed Agents 的 `auto` 权限策略：它会把工具调用评估为 `allow`、`ask` 或 `deny`，不是“自动进入人工审批”。客户端必须按 `evaluated_permission` 分流，保留 `evaluation` / `reason_code` 审计信息，并把强制人工审批的工具配置为 `always_ask`。

第二层变化是 `ant beta:sessions connect`：

- 终端 viewer 跟随主线程，可发消息、interrupt 和处理待确认工具；
- `--web` 在本地打开 viewer，可观察多 Agent 的全部线程；
- 非交互程序继续使用 events stream/send。

## 渠道 payload

| 渠道 | 本地文件 | 计划模式 | 标题/定位 |
| --- | --- | --- | --- |
| 博客园 | `cnblogs.md` | 待确认，默认远程草稿 | Managed Agents 的 auto 权限，不是“自动人工审批” |
| 掘金 | `juejin.md` | 待确认，默认远程草稿 | Managed Agents 权限处理：别把 auto 当成人工审批门 |
| V2EX | `v2ex.md` | 待确认，默认不发布 | `programmer` 节点讨论动态评估与人工门禁边界 |
| Bilibili | `bilibili.md` | 待确认，默认远程草稿 | 纯文本富文本结构，不含 Markdown 正文语法 |
| 小红书 | `xiaohongshu.md` | 待确认，默认不发布 | 1000 中文字符内短稿，当前无图片 |
| LinkedIn | `linkedin.md` | 待确认，默认不发布 | English operator note |

## 本地事实基线

- 本周上游范围：`41bbe19..34040c9`，1 个提交，1 个 Skill，7 个文件，+116/-16。
- 仓库规模：19 个本土化 Skill。
- `claude-api` 新增 2 个中文 few-shot、2 个正例与 1 个近似反例；触发集现为 14 个正例、7 个反例。
- 仓库 validator、quick validate、打包/ZIP、Python/Shell 语法、路由 smoke、上游事实 reference hash parity 与 `git diff --check` 已通过。
- 本机没有 `ant` CLI 或测试 session；未运行 `connect` / `--web`、`auto` 服务端三路判定、真实 Claude API 或任何工具副作用。

## 发布前确认项

每个平台都要在对应发布任务中重新确认：

1. 账号；
2. 最终标题与正文；
3. 标签、分类或 V2EX 节点；
4. 图片/封面；
5. 远程草稿、公开发布或提交审核模式；
6. 平台渲染预览截图与剩余风险。

没有最新确认时，只保留本地文件。不得创建远程草稿，不得点击发布或提交审核。
