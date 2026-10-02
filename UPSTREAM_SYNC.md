# 上游同步说明

上游仓库为 `https://github.com/anthropics/skills.git`，本地 remote 名称统一为 `upstream`。当前已审计至 `8a1541c`（2026-09-28），基线记录在 `sync/upstream-baseline.json`。

## 每周同步流程

1. 若工作区不干净，停止并报告，不覆盖人工改动。
2. `git fetch upstream main`，读取从上次基线到 `upstream/main` 的提交、文件和风险说明。
3. 按优先级处理：安全/数据损坏风险 > 脚本与 API 行为 > 新能力 > 文字整理。
4. 对脚本、许可证和事实性 reference 尽量保持上游原样；对 `SKILL.md` 依据 `LOCALIZATION.md` 做中文重构。
5. 更新中文触发词、真实中文 few-shot、近似反例及 `localization/trigger-evals.json`。
6. 运行 `python3 scripts/validate_repository.py`，并对受影响脚本执行对应 smoke test。
7. 更新基线 JSON，生成本次同步报告和多平台文章草稿；公开发布前必须人工确认预览。

## 冲突处理

- 不用上游英文 `SKILL.md` 直接覆盖中文版本。
- 若上游删除脚本，先替换所有调用方，再删除旧文件。
- 若本土化规则和上游事实冲突，以事实与安全为先，再调整中文表达。
- 单次改动过大时按 Skill 拆分，确保每个提交都能独立验证和回滚。

## 提交建议

同步提交使用：

```text
sync(<skill>): 对齐 upstream <short-sha> 并完成中文本土化
```

提交正文记录上游范围、中文改造点、验证结果和仍保留的英文 reference。
