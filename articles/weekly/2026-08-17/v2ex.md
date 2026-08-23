---
title: 模型升级后，大家怎么审计仓库里积累多年的 Prompt 补丁？
node: programmer
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

最近同步 Anthropic skills 的 `claude-api`，看到一个挺实用的新入口：`prompt-audit`。

它针对一个常见问题：模型 ID 和 API 参数升级了，但 system prompt、工具描述、few-shot 和 request builder 里还留着旧模型时代的补丁，例如大量强调、固定思考脚手架、assistant prefill、JSON 解析重试和一步不差的判断流程。

比较打动我的不是“删 Prompt”，而是它把审计约束成两份产物：

1. Findings 报告，每条必须有 file:line、命中模式、为何对目标模型过时、置信度和行动。
2. Proposed diff，只放高/中置信度修改，一个 finding 一个 hunk；低置信度只标记。

它还有一份很强的 keep list：业务上下文、工具契约、脆弱操作的精确步骤、仍能复现的禁止项都不能因为“太长”而删。没有发现时输出空 diff 也是有效结果。

skills-zh 这次保留 219 行事实 reference 原样，只重写中文触发和 few-shot：一个是清理 Claude 3.5 时代累积的客服 Prompt，另一个是迁移 Opus 5 后收尾 prefill 和工具描述。评测里还加了近似反例——纯翻译且要求结构不变，不应自动扩成审计。

仓库层可以用 validator、quick validate 和 Skill 打包检查同步完整性；真正有争议的删除，仍需要在目标模型上做 before/after probe。

大家现在会怎么维护 Prompt 的“版本债务”？是跟模型迁移一起审计，还是靠线上失败再追加/删除规则？有没有比较稳定的 provenance 或回归评测做法？

项目：https://github.com/MarcelLeon/skills-zh
