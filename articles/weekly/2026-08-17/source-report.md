# 2026-08-17 上游同步证据报告

## 结论

本周新增 1 个实质上游提交：Anthropic `f6656c1256d5a8adfa37db9110046ef20bac644c`（2026-08-13），标题为 `Update claude-api skill: prompt-audit subcommand (#1557)`。相对上次已处理的 `f17010c`，变化集中在 `claude-api` 3 个文件，上游 diff 为 227 行新增、3 行删除。

核心能力是 `prompt-audit`：它不是普通“提示词精简”，而是一套面向目标 Claude 模型的非交互审计流程。流程会盘点完整 Prompt surface、结合 Git provenance 判断历史补丁，再按已命名模式区分旧模型遗留指令与仍然承载业务事实的内容，最后同时交付 findings 报告和 proposed diff。

## 上游变化

1. 新增 `shared/prompt-audit.md`，覆盖 system prompt、Skill/规则文件、工具描述、few-shot、请求构造代码与模型参数。
2. 审计从请求和仓库推断范围与目标模型，不因缺少交互确认而停住；假设写进报告，便于重跑纠正。
3. findings 必须包含 `file:line`、证据、命中的模式、为何对目标模型过时、置信度与行动。
4. proposed diff 只处理高/中置信度项；低置信度只报告。没有发现时允许输出空 diff，禁止为了显得有产出而制造删除。
5. keep list 明确保留业务上下文、工具契约、脆弱操作的精确顺序、当前仍可复现的约束和格式敏感示例。
6. `migrate` 流程在完成模型/API breaking changes 后继续审计 Prompt、工具描述与 request builder。

## 中文本土化决策

- `description` 新增“提示词是否过时”“清理 prompt cruft”“旧模型 Prompt/Skill/tool description 审计”“模型迁移后检查提示词行为”等正式、口语和中英混输触发。
- 中文入口新增两个真实 few-shot：Claude 3.5 时代客服 Prompt 清理，以及 Sonnet 4.6 迁移 Opus 5 后收尾 prefill、思维脚手架与工具描述。
- 新增中文 `migrate` / `prompt-audit` 路由，保留上游“非交互审计、双产物、显式授权才改文件”的边界。
- `localization/trigger-evals.json` 增加 2 个 should-trigger 和 1 个近似 should-not-trigger；翻译提示词但要求结构不变时不应自行扩展为审计。
- 219 行事实性 reference 与上游原样一致；英文 `SKILL.md` 没有覆盖中文入口。
- marketplace、README、同步文档与基线更新到 `f6656c1`。

## 可复现命令

```bash
python3 scripts/upstream_diff_report.py --base f17010c9bb483898c1d9c9f42dde2b3a98889434 --head f6656c1256d5a8adfa37db9110046ef20bac644c
python3 scripts/validate_repository.py
python3 skills/skill-creator/scripts/quick_validate.py skills/claude-api
PYTHONPATH=skills/skill-creator python3 -m scripts.package_skill skills/claude-api /tmp/skill-dist
python3 -m compileall scripts skills/claude-api
find skills -name '*.sh' -exec bash -n '{}' +
```

## 验证状态与限制

本轮使用隔离的 Python 3.11.14 环境安装 `requirements-dev.txt`，`pip check` 无依赖冲突。验证结果：

- `scripts/validate_repository.py` 通过：`Repository validation passed: 17 localized skills`。
- `claude-api` quick validate 与 `.skill` 打包通过；ZIP 中包含 219 行 `shared/prompt-audit.md` 和中文入口。
- `python3 -m compileall scripts skills/claude-api` 与全仓 Skill Shell `bash -n` 通过。
- 除中文 `SKILL.md` 外，`skills/claude-api` 全部事实性文件与 `upstream/main` 无差异。
- 代表性 smoke test 验证 `prompt-audit` 双产物/keep list 路由、2 个新增正例与 1 个新增反例；`claude-api` 当前共 8 个正例、4 个近似反例。
- 6 个平台 payload 全部通过 `prepare_article_pack.py`；小红书正文 224 个中文字符。唯一警告是 `images: []`，后续图文发布可能要求媒体。
- `git diff --check` 通过。

上游变化是 Markdown/reference，没有新增可直接运行的 API 代码。

本轮不会调用真实 Claude 模型执行 before/after Prompt 行为评测，因此不能宣称每一种 dated pattern 的行为退化已在当前账号和目标模型上复现。`prompt-audit.md` 自身也要求：删除是需要行为 probe 验证的假设，不是仅凭文本匹配即可成立的结论。

## 发布门禁

文章包只保存在本地分支。没有打开平台编辑器、创建远程草稿或执行公开发布；每个平台仍需核对账号、最终标题、正文、标签/分类/节点、发布模式与真实渲染预览，并在对应发布任务中获得最新明确确认。
