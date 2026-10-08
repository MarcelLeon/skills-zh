# 2026-10-07 发布计划

## 当前状态

本地文章包已生成。博客园、小红书、Bilibili、掘金、V2EX 与 LinkedIn 共 6 个 payload 无错误；小红书正文 472 字符、218 个中文字符，唯一警告是没有声明图片。

没有打开任何平台编辑器，没有创建或覆盖远程草稿，也没有执行公开发布。

## 内容主轴

主角是 Managed Agents 从 quickstart 名称或 URL 上手时的证据与权限边界：精确匹配模板、区分 first-party/third-party、页面只作数据、先提案后写入、`ant apply` 先 dry-run、deployment 创建后先暂停。

## 渠道 payload

| 渠道 | 本地文件 | 计划模式 | 标题/定位 |
| --- | --- | --- | --- |
| 博客园 | `cnblogs.md` | 待确认，默认远程草稿 | 从 quickstart 或 URL 搭 Managed Agent，先把来源与权限边界讲清楚 |
| 掘金 | `juejin.md` | 待确认，默认远程草稿 | 从 URL 搭 Managed Agent，为什么必须先做来源分级 |
| V2EX | `v2ex.md` | 待确认，默认不发布 | `programmer` 节点讨论“可复制”的信任边界 |
| Bilibili | `bilibili.md` | 待确认，默认远程草稿 | 富文本友好的纯文本结构，不含 Markdown 正文语法 |
| 小红书 | `xiaohongshu.md` | 待确认，默认不发布 | 1000 中文字符内短稿，当前无图片 |
| LinkedIn | `linkedin.md` | 待确认，默认不发布 | English operator note |

## 本地事实基线

- 本轮上游范围：`8a1541c..683bc88`，1 个提交、1 个 Skill、18 个文件、+920/-16。
- 仓库规模：19 个本土化 Skill。
- `claude-api` 新增 2 个中文 few-shot、3 条 onboarding 子命令路由、2 个正例和 1 个近似反例；当前 19 个正例、8 个反例。
- 17 个变化的事实性 reference 和模板保持上游内容；中文入口保留本土化组织。
- 仓库 validator、quick validate、打包/ZIP、Python/Shell 语法和 onboarding 结构 smoke 已通过。
- 6 个平台 payload 无错误；小红书低于 1000 中文字符上限，当前无图片。
- 未安装 `ant` CLI，未连接真实 Claude Platform 工作区，未创建 Agent、session、deployment 或执行外部 MCP 写入。

## 发布前确认项

每个平台都要在对应发布任务中重新确认：

1. 账号；
2. 最终标题与正文；
3. 标签、分类或 V2EX 节点；
4. 图片/封面；
5. 远程草稿、公开发布或提交审核模式；
6. 平台渲染预览截图与剩余风险。

没有最新确认时，只保留本地文件。不得创建远程草稿，不得点击发布或提交审核。
