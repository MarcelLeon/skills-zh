# 2026-09-07 上游同步证据报告

## 结论

Anthropic Agent Skills 上游从已审核的 `3b3fad96af16a10759d930941b4520ba0c40edae` 前进到 `41bbe19d1a1a7eaab5e7bb9050a417e5c6cffc8f`。本周新增 2 个提交，影响 2 个 Skill、70 个文件，diff 为 2787 行新增、1804 行删除。

本周的实质能力变化是：

1. `claude-api` 新增以真实 Usage/Cost 数据为起点的 `cost-optimize` 工作流，以及组织成员、工作区、API key、服务账号、WIF、CMEK 等 Admin API 参考。
2. `claude-api` 更新 Fable/Mythos 5.1、Managed Agents、模型迁移、平台差异和七种语言 SDK 的事实性资料。
3. `frontend-design` 把统一圆角卡片、全大写眉题、单词变色、散落入场动画等通用默认列成明确的反模板检查。

`scripts/upstream_diff_report.py` 从当前主工作区旧基线 `b29e7cf` 扫到 `41bbe19` 时报告 8 个累计提交、4 个累计变化 Skill，未命中风险关键词。由于 2026-08-24 的已验证分支尚未进入 `origin/main`，本次实际本土化增量以 `3b3fad9..41bbe19` 为准，并在新分支中重放旧批次后继续工作，避免遗漏或覆盖主工作区。

## 上游范围

| Commit | 日期 | 变化 |
| --- | --- | --- |
| `5304866` | 2026-09-01 | 更新 `claude-api`：Fable/Mythos 5.1、Managed Agents、`cost-optimize`、Admin API 与多语言参考；69 个文件，+2751/-1784 |
| `41bbe19` | 2026-09-03 | 更新 `frontend-design`：扩展反通用化设计规则；1 个文件，+36/-20 |

## claude-api：先建立成本证据，再讨论降模型

新增 `shared/cost-optimization.md` 把降本拆成四步：先确认范围、质量门槛与基线；再从 Usage/Cost Admin API、应用自身的 `response.usage` 日志或代码估算中选择证据层级；然后按节省上限排序；最后一次只应用一个 lever，并以完成任务的成本和质量结果决定保留或回滚。

应用顺序先于排名顺序：Prompt Caching、输入 token、Agent 循环卫生、输出 token 和可异步任务的 Batch 属于 free wins；effort、预算、模型选择和多模型路由属于质量 tradeoff。真实模型运行会产生费用，因此中文入口明确要求先估算测试矩阵和预算，获得确认后才运行。

新增 `shared/admin-api.md` 则区分三类凭据：普通 Messages API key、Admin API key 与 `org:admin` OAuth。Admin API 管组织而不发送消息；服务账号与 WIF 等 OAuth-only 端点不能用 admin key 替代。中文入口增加了组织管理 few-shot，要求先交付最小权限与 dry-run/只读方案。

Fable/Mythos 5.1 的迁移也不能退化成模型 ID 替换。入口把 forced tool use、append-only history、thinking block 回放、`stop_reason: refusal`、fallback、长请求 streaming/timeout 与平台支持矩阵列为必须检查的迁移面。具体模型 ID、价格、beta header 和发布状态仍由上游 reference 或官方实时来源给出，不在中文入口复制一份易过期表格。

## frontend-design：把“模板味”变成可检查项

中文入口保留“从主题材料和真实内容出发”的主线，并新增两组真实场景：投研财务看板与中文品牌故事页。设计计划允许使用一个字体家族；若用两个则必须角色明显，正文默认控制可读行长，中文长标题需要在真实移动视口验证。

反模板审查新增以下近似默认：

- 所有层级都变成同款圆角卡片、灰色阴影和装饰渐变；
- 全大写眉题、中点连接元信息、`WORD — fragment` 标签、小号等宽标签和按钮末尾箭头不分主题复用；
- 标题只挑一个词改斜体、粗体或强调色；
- 每段淡入上滑、每张卡片 hover，而非用动效解释用户操作后的状态变化。

这些不是绝对禁用项；用户 brief 明确需要时仍应服从 brief。验收重点是每个视觉选择能否解释为当前主题和任务服务。

## 中文本土化验收

- `claude-api` description 新增成本优化、Admin API、Fable/Mythos 与 Microsoft Foundry 等自然触发表达；新增 3 个中文 few-shot。
- `frontend-design` 新增 2 个中文 few-shot和 1 个文字校对近似反例。
- `localization/trigger-evals.json` 中，`claude-api` 当前为 12 个 `should_trigger`、6 个 `should_not_trigger`；`frontend-design` 为 4 个正例、2 个反例。
- 上游 68 个 `claude-api` 支撑文件保持事实内容一致；`shared/platform-availability.md` 仅去除上游文件尾多余空行，以通过 diff hygiene。
- 中文 `SKILL.md` 没有被英文入口覆盖。

## 验证证据

- Python 3.11 隔离环境成功安装 `requirements-dev.txt`，`pip check` 无损坏依赖。
- `python3 scripts/validate_repository.py`：`Repository validation passed: 19 localized skills`。
- `claude-api` 与 `frontend-design` 的 `quick_validate.py` 均通过。
- 全仓 Python `compileall` 与所有 Skill Shell 的 `bash -n` 通过。
- 两个 Skill 均成功打包，`unzip -t` 无错误。
- 中文路由 smoke、JSON 语法、除已说明文件尾空行外的上游事实文件 hash parity 与 `git diff --check` 通过。
- 6 个平台 payload 经 `prepare_article_pack.py` 验证均无错误；小红书正文 663 字符、中文 242 字，唯一警告是没有图片。

## 分支关系与限制

新分支 `codex/weekly-skills-zh-2026-09-07` 从 `origin/main` 创建，先重放 2026-08-24 已验证提交，再叠加本周同步。旧批次未合入，因此这个分支包含待交付的 2026-08-24 与 2026-09-07 两轮内容；PR 中必须说明替代关系，避免未来把旧分支和新分支同时合入。

本轮没有调用真实 Claude API，没有读取真实组织 Usage/Cost 数据，没有执行 Admin API 写操作，也没有对 Fable/Mythos 5.1 做运行时请求或模型级触发 A/B。通过的是仓库、本土化、参考资料一致性、语法、分发包和确定性路由 smoke，不等于上述线上能力已端到端实测。
