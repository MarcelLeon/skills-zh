# 2026-09-07 发布计划

## 当前状态

本地文章包已生成。博客园、小红书、Bilibili、掘金、V2EX 与 LinkedIn 共 6 个 payload 已通过 `prepare_article_pack.py`，无错误；小红书正文 663 字符、中文 242 字，唯一警告是未声明图片。

没有打开任何平台编辑器，没有创建或覆盖远程草稿，也没有执行公开发布。

## 内容主轴

主角是 `claude-api cost-optimize`：把“换便宜模型”改造成范围、质量门槛、token profile、按节省上限排序、free wins 优先、逐 lever diff 与付费评测确认组成的证据链。

第二层变化包括：

- Admin API 组织管理与普通 API key、Admin key、`org:admin` OAuth 的边界；
- Fable/Mythos 5.1 的 forced tool use、thinking 回放、append-only history 和 refusal fallback 迁移面；
- `frontend-design` 对 SaaS 卡片套件、通用字体处理和散落动效的反模板审查。

## 渠道 payload

| 渠道 | 本地文件 | 计划模式 | 标题/定位 |
| --- | --- | --- | --- |
| 博客园 | `cnblogs.md` | 待确认，默认远程草稿 | Claude API 降本，先别急着换便宜模型 |
| 掘金 | `juejin.md` | 待确认，默认远程草稿 | Claude API 成本优化：先做 token profile，再决定要不要换模型 |
| V2EX | `v2ex.md` | 待确认，默认不发布 | `programmer` 节点讨论 cost per task 与降本顺序 |
| Bilibili | `bilibili.md` | 待确认，默认远程草稿 | 纯文本富文本结构，不含 Markdown 正文语法 |
| 小红书 | `xiaohongshu.md` | 待确认，默认不发布 | 1000 中文字符内短稿，当前无图片 |
| LinkedIn | `linkedin.md` | 待确认，默认不发布 | English operator note |

## 本地事实基线

- 本周上游范围：`3b3fad9..41bbe19`，2 个提交，2 个 Skill，70 个文件，+2787/-1804。
- `5304866`：`claude-api` 69 个文件，+2751/-1784。
- `41bbe19`：`frontend-design` 1 个文件，+36/-20。
- 仓库规模：19 个本土化 Skill。
- 仓库 validator、两个 Skill 的 quick validate/打包/ZIP、Python/Shell 语法、路由 smoke 与上游事实一致性已通过。
- 未调用真实 Claude API，未读取真实账单，未执行 Admin API 写操作，未做模型触发 A/B。

## 发布前确认项

每个平台都要在对应发布任务中重新确认：

1. 账号；
2. 最终标题与正文；
3. 标签、分类或 V2EX 节点；
4. 图片/封面；
5. 远程草稿、公开发布或提交审核模式；
6. 平台渲染预览截图与剩余风险。

没有最新确认时，只保留本地文件。不得创建远程草稿，不得点击发布或提交审核。
