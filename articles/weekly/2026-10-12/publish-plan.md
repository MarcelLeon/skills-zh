# 2026-10-12 发布计划

## 当前状态

本地文章包已生成。6 个平台 payload 无错误；小红书正文 669 字符、207 个中文字符，唯一警告是未声明图片。没有打开任何平台编辑器，没有创建或覆盖远程草稿，也没有执行公开发布。

## 内容主轴

主角是 Managed Agents dynamic workflows 的规模判断：roster 适合若干独立任务，整项工作碎片多到会超过 25 个 child thread、必须分批时才切 workflow run。文章同时解释预算告知、条件式 system prompt、关闭方式、单问单答不过度编排，以及 `limited.allowed_hosts` 对网页工具的新边界。

Haiku 5.5 是同轮 API 迁移事项，作为次要章节说明“不能只换模型 ID”。

## 渠道 payload

| 渠道 | 本地文件 | 计划模式 | 标题/定位 |
| --- | --- | --- | --- |
| 博客园 | `cnblogs.md` | 待确认，默认远程草稿 | 25 个子线程不够时，Managed Agents 该用 dynamic workflows 了 |
| 掘金 | `juejin.md` | 待确认，默认远程草稿 | 实现型文章：配置、system prompt、预算与关闭方式 |
| V2EX | `v2ex.md` | 待确认，默认不发布 | `programmer` 节点讨论 roster→workflow 阈值 |
| Bilibili | `bilibili.md` | 待确认，默认远程草稿 | 富文本友好纯文本，无 Markdown 正文围栏 |
| 小红书 | `xiaohongshu.md` | 待确认，默认不发布 | 1000 中文字符内短稿，当前无图片 |
| LinkedIn | `linkedin.md` | 待确认，默认不发布 | English operator note |

## 本地事实基线

- 上游范围：`683bc88..dbd4588`，2 个提交、1 个 Skill、54 个文件、+1812/-413。
- 仓库规模：19 个本土化 Skill；marketplace 版本 `1.0.7`。
- `claude-api` 新增 3 个中文 few-shot、3 个正例和 1 个近似反例；当前 22 个正例、9 个反例。
- 52 个变化的事实性文件与上游 Git blob 一致；`cost-hillclimb.md` 只做 4 处行尾空格归一化；中文入口保留本土化结构。
- Python 3.11.14 requirements 与 `pip check`、仓库 validator、quick validate、打包/ZIP、compileall、2 个 Shell 脚本 `bash -n`、特性与 parity smoke、`git diff --check` 已通过。
- 博客园、小红书、Bilibili、掘金、V2EX、LinkedIn 共 6 个 payload 无错误；小红书低于 1000 中文字符上限，当前无图片。
- 未安装 Managed Agents `ant` CLI，未连接真实 Claude Platform 工作区，未启动 workflow run，未调用 Haiku 5.5，未创建 Agent/session/deployment。

## 发布前确认项

每个平台都要在对应发布任务中重新确认：

1. 账号；
2. 最终标题与正文；
3. 标签、分类或 V2EX 节点；
4. 图片/封面；
5. 远程草稿、公开发布或提交审核模式；
6. 平台渲染预览截图与剩余风险。

没有最新确认时，只保留本地文件。不得创建远程草稿，不得点击发布或提交审核。
