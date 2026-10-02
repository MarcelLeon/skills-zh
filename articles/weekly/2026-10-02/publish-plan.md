# 2026-10-02 发布计划

## 当前状态

本地文章包已生成。博客园、小红书、Bilibili、掘金、V2EX 与 LinkedIn 共 6 个 payload 无错误；小红书正文 525 字符、205 个中文字符，唯一警告是没有声明图片。

没有打开任何平台编辑器，没有创建或覆盖远程草稿，也没有执行公开发布。

## 内容主轴

主角是 Claude 应用的可审计 eval/hillclimb 闭环：先确认输入、runner 与 grader，再审计评测健康度；用 train/validation/test 隔离调优与最终判断，并把每轮 diff、质量、token/费用、失败样本和停止条件一起记录。

第二层变化包括：

- 上游示例默认更新为 Claude Opus 5.5，并加入 Claude Sonnet 5.5 的迁移事实；
- 新增 preserved-thinking migration 指南、`prefix_diff.py` 和 `drop_block_probe.py`；
- streaming client tools 的 `eager_input_streaming` 需要客户端在执行工具前验证完整 JSON 和 schema；
- refusal billing 的说明链接到官方文档。

## 渠道 payload

| 渠道 | 本地文件 | 计划模式 | 标题/定位 |
| --- | --- | --- | --- |
| 博客园 | `cnblogs.md` | 待确认，默认远程草稿 | 别再挑成功案例：给 Claude 应用补一条可审计的 eval 闭环 |
| 掘金 | `juejin.md` | 待确认，默认远程草稿 | Claude 应用调 Prompt，先把 eval 做成可审计闭环 |
| V2EX | `v2ex.md` | 待确认，默认不发布 | `programmer` 节点讨论 test 集隔离与 grader 过拟合 |
| Bilibili | `bilibili.md` | 待确认，默认远程草稿 | 纯文本富文本结构，不含 Markdown 正文语法 |
| 小红书 | `xiaohongshu.md` | 待确认，默认不发布 | 1000 中文字符内短稿，当前无图片 |
| LinkedIn | `linkedin.md` | 待确认，默认不发布 | English operator note |

## 本地事实基线

- 本轮上游范围：`34040c9..8a1541c`，2 个提交、1 个 Skill、72 个文件、+6982/-620。
- 仓库规模：19 个本土化 Skill。
- `claude-api` 新增 3 个中文 few-shot、3 个正例和 1 个近似反例，并修正 1 条模型迁移路由歧义。
- 71 个变化的事实性支撑文件保持上游事实、命令与代码行为；其中 16 处行尾空格/末尾空行做纯空白归一化，中文入口保留本土化组织。
- 仓库 validator（19 Skills）、quick validate、打包/ZIP、Python/Shell/Node 语法、17 正例/7 反例路由、诊断脚本 dry-run、报告构建 smoke 与六平台 payload 已通过。
- 没有付费预算确认，不运行真实 Claude API、eval/hillclimb 或 preserved-thinking replay。

## 发布前确认项

每个平台都要在对应发布任务中重新确认：

1. 账号；
2. 最终标题与正文；
3. 标签、分类或 V2EX 节点；
4. 图片/封面；
5. 远程草稿、公开发布或提交审核模式；
6. 平台渲染预览截图与剩余风险。

没有最新确认时，只保留本地文件。不得创建远程草稿，不得点击发布或提交审核。
