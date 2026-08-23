# 2026-08-10 上游同步证据报告

## 结论

本周有 1 个实质上游提交：Anthropic `f17010c9bb483898c1d9c9f42dde2b3a98889434`（2026-08-07），标题为 `Update claude-api skill: Managed Agents August launch wave (#1532)`。变化集中在 `claude-api`，共 18 个文件，上游 diff 为 328 行新增、59 行删除。

本次不是逐句翻译。17 个事实性 reference 按上游原样同步，中文 `SKILL.md` 重新组织触发、真实任务路由和边界，未被英文入口覆盖。

## 上游能力变化

1. Session budget：创建 session 时可设置按公开价计算的美元硬上限；达到上限后以 `budget_reached` 暂停，只有修改或移除预算才能恢复。
2. Deployment budget：预算复制到后续每次触发的 session；与 session 不同，部署预算可以清除后重新加入。
3. Inference geo：Managed Agents 在 `model.inference_geo` 中设置，并要求 multiagent roster 的 geo 一致。
4. Repository Skills：cloud sandbox 在 session 启动时发现仓库根目录 `.claude/skills/<skill-name>/`；只扫描一次，仓库提交权限因此属于 Agent 指令信任边界。
5. Advisor 与 multiagent：新增 Advisor roster 入口、thread event 交付规则，以及从 `self`、低成本 worker 到专门角色的分工建议。
6. 事实纠错：agent version 改为顺序整数；Files API 上传补 `purpose`；`vault_ids` 明确为 session create-only；deployment 增加 update；refusal category 改为开放集合；Sonnet 5 加入 prefill 已移除范围。

## 中文本土化决策

- `description` 新增 session/deployment 预算、`inference_geo`、Advisor、多 Agent、GitHub 仓库 Skills 的正式说法和中英混输词。
- 新增 3 个中文 few-shot：25 美元代码审查预算、US inference + Advisor、仓库 Skills 与指令注入边界。
- 新增 Managed Agents 能力分流，明确 session budget 与 Messages API `task_budget` 不是同一概念。
- `localization/trigger-evals.json` 为 `claude-api` 增加 4 个应触发案例，并增加普通云预算、OpenAI/LangGraph 多 Agent 等近似反例。
- marketplace、README、同步文档和基线更新到 `f17010c`。
- 打包 smoke test 发现旧文档命令会触发 `ModuleNotFoundError: No module named 'scripts'`，已改为从仓库根目录设置 `PYTHONPATH=skills/skill-creator` 后按模块运行，并复测通过。

## 可复现证据

上游范围：

```bash
python3 scripts/upstream_diff_report.py --base b29e7cf65e5cb78a5ac33d582270551bc74a14eb --head upstream/main
```

仓库与 Skill 验收：

```bash
python3 scripts/validate_repository.py
python3 skills/skill-creator/scripts/quick_validate.py skills/claude-api
PYTHONPATH=skills/skill-creator python3 -m scripts.package_skill skills/claude-api /tmp/skill-dist
python3 -m compileall scripts skills/claude-api
find skills -name '*.sh' -exec bash -n '{}' +
```

本次结果：仓库校验通过 17 个本土化 Skill；`claude-api` quick validate 通过；Python 语法检查通过；全仓 Shell `bash -n` 通过；打包通过并生成 `claude-api.skill`；17 个事实性 reference 与 `upstream/main` 对比无差异。

## 验证限制

上游提交本身是 Markdown/reference 同步，没有可直接离线运行的新业务脚本。本次代表性 smoke test 覆盖结构、路径、打包、Python/Shell 语法和上游 reference 一致性；未调用真实 Managed Agents beta API，因此没有宣称预算暂停、geo pin 或 Advisor 的线上行为已经在当前账号实测。

## 发布状态

文章包只保存在本地。尚未执行任何平台编辑器预览、远程草稿或公开发布；账号、最终标题、正文、标签和发布模式都需要用户在对应发布任务中查看平台预览后再次确认。
