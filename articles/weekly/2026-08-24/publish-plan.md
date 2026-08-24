# 2026-08-24 发布计划

## 当前状态

本地文章包已生成。博客园、小红书、Bilibili、掘金、V2EX 与 LinkedIn 共 6 个 payload 已通过 `prepare_article_pack.py`，无错误；小红书正文 664 字符、中文 230 字，唯一警告是未声明图片。

没有打开任何平台编辑器，没有创建或覆盖远程草稿，也没有执行公开发布。

## 内容主轴

主角是 `claude-api upgrade`：把 Python `anthropic` SDK 0.x→1.x 从“改版本号和 import”升级成一条带范围确认、可搜索 inventory、`[BREAKS]`/`[DECIDE]` 分层、验证与限制报告的证据链。

两项新增 Skill 作为本周第二层变化：

- `academy-guide` 只在强学习意图下推荐实时 Academy 内容。
- `discernment-nudge` 只在可行动的实质答案后追加一次具体辨别问题。

## 渠道 payload

| 渠道 | 本地文件 | 计划模式 | 标题/定位 |
| --- | --- | --- | --- |
| 博客园 | `cnblogs.md` | 待确认，默认远程草稿 | Anthropic Python SDK 1.x 升级，不只是把版本号改成 1.0 |
| 掘金 | `juejin.md` | 待确认，默认远程草稿 | 从 httpx2 到 Bedrock region：把 Anthropic SDK 1.x 升级做成可验证流程 |
| V2EX | `v2ex.md` | 待确认，默认不发布 | `programmer` 节点讨论 SDK major upgrade 的自动化边界 |
| Bilibili | `bilibili.md` | 待确认，默认远程草稿 | 纯文本富文本结构，不含 Markdown 正文语法 |
| 小红书 | `xiaohongshu.md` | 待确认，默认不发布 | 1000 中文字符内短稿，当前无图片 |
| LinkedIn | `linkedin.md` | 待确认，默认不发布 | English operator note |

## 本地事实基线

- 上游范围：`f6656c1..3b3fad9`，4 个提交，3 个 Skill，9 个文件，+1081/-6。
- 仓库规模：19 个本土化 Skill。
- SDK live smoke：截至 2026-08-24，`anthropic 1.0.0` 已发布；隔离安装验证 `Requires-Python >=3.10` 与 `httpx2 2.12.0`。
- 未执行真实 Claude API 请求、真实 0.x 项目升级或模型触发 A/B。
- Academy `catalog.json` 直取超时，不能宣传具体实时课程推荐已跑通。

## 预览证据门禁

进入任一平台前，需要用户对以下内容给出最新明确确认：

1. 渠道与准确账号。
2. 最终标题、正文、标签、分类或 V2EX 节点。
3. 草稿、提交审核或公开发布模式。
4. 小红书是否补图片；当前 `images: []`，图文发布可能要求媒体。
5. 是否允许创建或更新远程草稿。

获得上述确认后，只填充已批准 payload，使用平台真实预览或最终提交前页面核对标题、正文格式、链接、标签、封面与模式，并采集足够截图。公开发布前仍需在当前会话再次确认最终按钮。

历史平台登录、账号激活和发布状态可能已变化，必须实时重查，不能沿用旧任务结论。
