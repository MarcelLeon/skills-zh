# 2026-10-02 上游同步证据报告

## 结论

Anthropic Agent Skills 上游从已审核的 `34040c9c568585f6929bedeaad110ad08f079624` 前进到 `8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4`。实际增量为 2 个提交，只影响 `claude-api`，共 72 个文件、6982 行新增、620 行删除。

本轮主角不是模型名称更新本身，而是把“凭感觉调 Prompt”变成一条可审计的评测闭环：上游新增 build-eval、eval-audit、eval-hillclimb、cost-hillclimb、报告 schema、轻量 HTML report builder 和 runner scaffold。同时补齐 Claude Opus 5.5 / Sonnet 5.5 的模型迁移事实、preserved-thinking 迁移指南与两份诊断脚本，并把 streaming client tools 的 `eager_input_streaming` 风险写入语言示例。

## 上游范围

| Commit | 日期 | 变化 |
| --- | --- | --- |
| `3337550` | 2026-09-24 | 将 refusal billing 的说明链接到官方文档；4 个文件，+7/-7 |
| `8a1541c` | 2026-09-28 | Claude Opus 5.5 / Sonnet 5.5、eval/hillclimb、preserved-thinking migration、eager input streaming 等；72 个文件，+6976/-614 |

`scripts/upstream_diff_report.py --base 34040c9` 确认本轮实际只有上述 2 个提交、1 个变化 Skill。主工作区未切换；所有写入位于独立 worktree 和 `codex/weekly-skills-zh-2026-10-02` 分支。

## 新增评测闭环

上游新增的 eval 资料不是一份泛化教程，而是一组可执行约束：

1. `shared/evals/build-eval.md` 要先明确被评测的应用、输入来源和评分方式；真实 API 运行前必须测出单次成本，并让用户确认输入、grader 与预算。
2. `shared/evals/eval-audit.md` 检查 task、harness、metrics 和 grader 是否能测出目标变化，避免“全是容易样本”“只看平均分”或 grader 泄漏。
3. `shared/evals/eval-hillclimb.md` 用 train/validation/test 分割约束迭代；每轮记录改动、分数、token/费用与停止条件，test 不是调参素材。
4. `shared/evals/cost-hillclimb.md` 把质量线与费用放在同一实验记录中，不用单价猜“更省”。
5. `shared/evals/report/build-report-lite.mjs`、`SCHEMA.md` 和 `runner-scaffold.mjs` 给出可复用的状态、报告与执行骨架，避免每次临时写不可比较的看板。

## 模型与运行时迁移

上游示例默认模型更新为 Claude Opus 5.5（`claude-opus-5-5`），并加入 Claude Sonnet 5.5。迁移指南强调不能只替换 model id：

- Opus 5.5 和 Sonnet 5.5 的 thinking/effort 约束需要按目标模型处理；旧项目显式发送 `thinking: {type: "disabled"}` 时不能沿用旧假设。
- forced tool use、Advisor 配对、task budget、mid-conversation system message 和平台可用性都有模型级差异。
- streaming + client tools 可启用 `eager_input_streaming: true`，但开启后客户端必须验证累积工具参数；截断或坏 JSON 不能进入有副作用的工具。

## Preserved thinking 迁移

`shared/preserved-thinking-migration.md` 把历史消息前缀问题拆成可测步骤：先用三请求自检证明检查已生效，再捕获连续请求并用 `prefix_diff.py` 找前缀变化；真实 replay 前先 dry-run、估算费用并确认预算。`drop_block_probe.py` 可先走 token-counting endpoint 找 400，再在受控样本上测 `drop_block`。

结果按 conversation 统计新的 dropped blocks，不能把同一个失效 thinking block 在后续每轮的重复出现算成多个根因。每个原因独立成 diff，复测后再决定保留或撤销；“样本确实 replay 了 thinking 且没有 drop，因此无需修改”是有效结论。

## 中文本土化验收

- `description` 新增 Opus/Sonnet 5.5、build-eval、eval audit、hillclimb、preserved thinking 与 `eager_input_streaming` 的正式、口语和中英混输触发。
- 新增 3 个真实中文 few-shot：5.5 模型迁移、脱敏工单 eval/hillclimb、大参数工具输入流式校验。
- 新增 `build-eval`、`preserved-thinking-migration`、`hillclimb` 子命令路由。
- `localization/trigger-evals.json` 新增 3 个 `should_trigger` 与 1 个本地正则 eval 近似反例，并修正“只迁移模型、不升级 SDK”仍应触发 `claude-api` 的旧歧义。
- 71 个变化的事实性支撑文件保持上游事实、命令与代码行为；其中 16 处上游行尾空格/末尾空行按仓库门禁做纯空白归一化，中文 `SKILL.md` 没有被英文入口覆盖。

## 验证证据

- Python 3.11.14 隔离环境安装 `requirements-dev.txt`，`pip check` 报告 `No broken requirements found`。
- `python3 scripts/validate_repository.py`：`Repository validation passed: 19 localized skills`。
- `claude-api` quick validate 通过；`.skill` 打包成功，`unzip -t` 无错误。
- `skills/claude-api` Python `compileall`、全仓 Skill Shell `bash -n`、两份新增 `.mjs` 的 `node --check` 全部通过。
- preserved-thinking smoke 使用 3 个合成请求：`prefix_diff.py` 正确把第一对判为 match，把重写 system 的第二对判为 `system_changed / system_rerendered`；`drop_block_probe.py --dry-run` 识别 2 个会 replay thinking 的请求、估算约 243 个输入 token，并明确 `nothing sent`。
- report builder smoke 从 2 个 variant、2 个 case 生成 `report.html` 与 `trajectory/scores.tsv`；train/test 两行分数与合成输入一致。
- 中文路由 smoke 通过：17 个 `should_trigger`、7 个 `should_not_trigger`，并命中 Opus 5.5、hillclimb、`eager_input_streaming` 与本地正则 eval 近似反例。
- 71 个事实性支撑文件保持上游事实、命令与代码行为；与 `upstream/main` 的额外差异仅为 16 处纯空白归一化，另有中文 `SKILL.md` 的有意本土化差异。
- 博客园、小红书、Bilibili、掘金、V2EX、LinkedIn 共 6 个 payload 无错误；小红书正文 525 字符、205 个中文字符，唯一警告是没有声明图片。
- `git diff --check` 与最终仓库复验通过。

## 证据边界

本轮不会为了验证文档而自动调用真实 Claude API。没有经过用户预算确认，不运行付费 eval、hillclimb 或 preserved-thinking replay；也不宣称 Opus 5.5 / Sonnet 5.5 的真实模型行为、账单变化或服务端平台兼容性已经在当前账号得到证明。
