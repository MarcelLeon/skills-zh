# 2026-08-24 上游同步证据报告

## 结论

本周上游从 `f6656c1256d5a8adfa37db9110046ef20bac644c` 前进到 `3b3fad96af16a10759d930941b4520ba0c40edae`，共 4 个提交，最终影响 9 个文件，diff 为 1081 行新增、6 行删除。

变化包含三个能力面：

1. 新增 `academy-guide`：只在用户明确想学习 Claude 产品时，从实时 Claude Academy 目录推荐强匹配内容。
2. 新增 `discernment-nudge`：在用户可能据此行动的实质答案后，最多一次追加 2–3 个具体辨别问题。
3. `claude-api` 新增 `upgrade`：当前提供 Python `anthropic` SDK 0.x→1.x 的逐项迁移指南。

仓库由 17 个本土化 Skill 增至 19 个。没有安全关键词提交命中，但 SDK 大版本升级包含运行兼容性风险；两个新 Skill 也都有容易误触发的相邻场景，因此本轮按“脚本/API 行为与边界 > 新能力 > 文字整理”处理。

## 上游范围

| Commit | 日期 | 变化 |
| --- | --- | --- |
| `89dcaa3` | 2026-08-17 | 新增 Claude Academy 导学 Skill |
| `f379e5a` | 2026-08-17 | 新增辨别提醒 Skill |
| `0a64e39` | 2026-08-18 | 将 `claude-academy-guide` 改名为可上传的 `academy-guide`，并把 description 缩到 1024 字符限制内 |
| `3b3fad9` | 2026-08-21 | 新增 Python SDK 0.x→1.x 升级指南与 `upgrade` 路由 |

`claude-api` 的 286 行升级指南把命中项分为 `[BREAKS]` 和 `[DECIDE]`。主要变化包括：

- Python 运行下限提升到 3.10，旧 CI matrix 是否一起调整必须由用户决定。
- SDK HTTP 层从 `httpx` 转到 `httpx2`；只有跨 SDK 边界的 client、transport、timeout、request/response 类型需要替换或做应用级 alias。
- async `with_raw_response` 的 `parse/json/text/read` 需要 `await`，sync 的 `text`/`content` 也从属性改成方法。
- Text Completions、`HUMAN_PROMPT`、`AI_PROMPT` 被移除，需要迁到 Messages API。
- sampling 参数、raw `output_format`、`parse(stream=)`、client-side compaction、raw bytes body、stream 类型检查等都有精确迁移规则。
- Bedrock 不再默默回退到 `us-east-1`；无法从部署配置证明 region 时只能报告待决定，不能猜。

## 中文本土化决策

### academy-guide

- description 覆盖“怎么用、从哪开始、能做什么、有没有教程/课程/培训材料”、团队推广、课堂上手，以及 Projects、Artifacts、Skills、连接器、MCP 等中英混输表达。
- 明确“学习意图”而非关键词才是触发条件；用户正在让 Agent 完成任务时不推荐课程。
- 保留先回答、强匹配、最多两项、只复制实时目录 URL、gated 内容提示登录、目录是数据不是指令、目录不可用时只给产品中心/资源库等边界。
- 新增团队学习 Claude Code、Projects 短教程两个中文 few-shot；增加“直接整理访谈稿”的近似反例。

### discernment-nudge

- description 覆盖可行动的建议、计划、提案、邮件、估算、数据解读和多步推理。
- 中文入口把“每会话最多一次”“用户已要求核验就跳过”“纯教学、代码、创作、格式转换与按用户材料整理跳过”写成显式决策树。
- 固定中文引导句为“有几件事值得再看一眼：”，问题必须绑定答案中的数字、假设或缺失上下文，并写成用户可直接追问的第一人称句子。
- 新增获客计划与竞业邮件两个中文 few-shot；增加“已要求逐项给出处”的近似反例。

### claude-api

- description 新增 SDK 大版本升级、Python `anthropic` 0.x→1.x、`httpx2`、Python 下限和 removed API 等触发。
- 中文入口加入一个范围明确的服务升级场景，以及一个 `/claude-api upgrade python` 范围不明、必须先确认的场景。
- 新增 `upgrade` 子命令与 reference 路由；明确 SDK 包升级不等于 Claude 模型迁移。
- 触发评测新增 2 个正例和 1 个模型迁移型近似反例。当前 `claude-api` 共 10 个正例、5 个反例。

marketplace 版本更新到 `1.0.2`，README、UPSTREAM_SYNC 与同步基线更新到 `3b3fad9`。

## 可复现命令

```bash
python3 scripts/upstream_diff_report.py \
  --base f6656c1256d5a8adfa37db9110046ef20bac644c \
  --head 3b3fad96af16a10759d930941b4520ba0c40edae

SKILLS_ZH_VALIDATOR_PYTHON=/path/to/python3.11 \
  /path/to/python3.11 scripts/validate_repository.py

python3.11 skills/skill-creator/scripts/quick_validate.py skills/academy-guide
python3.11 skills/skill-creator/scripts/quick_validate.py skills/discernment-nudge
python3.11 skills/skill-creator/scripts/quick_validate.py skills/claude-api
```

## 验证证据

- Python 3.11.14 隔离环境安装 `requirements-dev.txt` 成功，`pip check` 无冲突。
- 仓库 validator 通过：`Repository validation passed: 19 localized skills`。
- 三个受影响 Skill 的 quick validation、`.skill` 打包和 ZIP 完整性检查通过；`claude-api.skill` 包含 286 行 `sdk-upgrade.md`。
- `python -m compileall -q scripts skills/academy-guide skills/discernment-nudge skills/claude-api` 通过。
- 全仓 Skill Shell 的 `bash -n` 通过。
- 两份新 LICENSE、`claude-api` 的 README、`sdk-upgrade.md` 与 `shared/live-sources.md` 的 Git blob 与 `upstream/main` 完全一致。
- 确定性路由 smoke 通过：`academy-guide` 2 正/1 反、`claude-api` 10 正/5 反、`discernment-nudge` 2 正/1 反；description 长度分别为 283、639、241，均低于 1024。
- 2026-08-24 执行 `pip index versions anthropic`，确认最新已发布版本为 `1.0.0`；一次性 Python 3.11 环境安装后验证 `anthropic 1.0.0`、`httpx2 2.12.0`、`Requires-Python >=3.10`、`anthropic.Timeout` 可导入且依赖检查通过。没有调用真实 Claude API。
- 博客园、小红书、Bilibili、掘金、V2EX 与 LinkedIn 共 6 个 payload 全部通过 `prepare_article_pack.py`；小红书正文 664 字符，其中中文 230 字，唯一警告是 `images: []`。

## 明确限制

- 没有拿真实 0.x 项目执行完整升级，因此不能宣称每一种旧 call site、测试桩、APM 或 Bedrock 部署都已实迁成功。
- 没有运行模型级触发 A/B；JSON 正反例与内容断言证明的是本土化验收面完整，不等于任意模型都会 100% 命中。
- Claude Academy 官方站点与资源页可访问，但从当前 CLI 直取 `assets/data/catalog.json` 两次超时；本轮没有验证 `staleAfter`、目录 schema 或具体 item 推荐。运行时获取失败必须按 Skill 规则降级到官方产品中心或资源库，不能凭记忆给具体课程。
- 文章 payload 只验证本地结构和字符限制；没有平台真实渲染预览，小红书还没有图片。

## 发布门禁

文章包只保存在本分支。没有打开平台编辑器、创建或覆盖远程草稿、采集平台预览、提交审核或公开发布。

进入任一公开渠道前，仍需用户在对应发布任务中明确确认准确账号、最终标题、正文、标签/分类/节点、图片、草稿或公开模式，并授权创建远程草稿。填充后还要采集平台真实预览证据，在最终发布按钮前再次确认。
