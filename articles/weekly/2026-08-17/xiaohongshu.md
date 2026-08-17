---
title: Prompt不是越短越好
tags: [Claude, Prompt工程, AIAgent, 开发者工具]
images: []
---

模型升级了，Prompt 里的旧补丁升级了吗？

skills-zh 本周对齐 Anthropic f6656c1，给 claude-api 加入 prompt-audit。

它不做“删字比赛”，而是先盘点 system prompt、Skills、tool descriptions、few-shot 和 request builder，再结合 Git 历史判断：这条规则当初修复了哪个模型的什么问题？目标模型上还能复现吗？

每条 finding 都要有 file:line、命中模式、过时理由、置信度和行动；同时给 proposed diff。低置信度只标记，不直接改。

更重要的是 keep list：业务上下文、工具契约、合规边界、脆弱操作步骤和仍能复现的问题必须保留。没有发现时，空 diff 也是正确答案。

中文本土化新增两个真实任务：
1️⃣ 清理 Claude 3.5 时代累积的客服 Prompt；
2️⃣ 迁移 Opus 5 后收尾 prefill、思维脚手架和工具描述。

验证：17 个 Skill 仓库门禁、claude-api 打包、语法和平台 payload 已通过。

边界：仓库验证通过不等于行为已在线实测，真正删除前仍要做目标模型 before/after probe。

#Claude #Prompt工程 #AIAgent #开发者工具
