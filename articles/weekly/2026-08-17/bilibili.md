---
title: Prompt 不是越短越好：旧模型遗留指令审计方法
tags: [Claude, Prompt工程, Agent, 开发工具]
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---
Prompt 不是越短越好：旧模型遗留指令审计方法
上游版本：f6656c1
影响范围：claude-api 3 个文件
一、Prompt 也有版本债务
旧模型漏调用工具，就加一条强提醒；JSON 不稳定，就加 assistant prefill、stop sequence 和解析重试；输出爱跑偏，就塞一个固定示例。
模型和 API 升级后，这些补丁不会主动报错，却可能让新模型过度触发、过度规划或被旧输出结构锁住。
二、审计先盘点完整 surface
System prompt、工具描述、Skill、few-shot、模型参数和 request builder 都要纳入。只改 prompt 文本但保留旧请求分支，不算完成迁移。
三、每条 finding 都要有证据
报告必须给出 file:line、原文、命中的模式、为何对目标模型过时、置信度和行动。高、中置信度项进入 proposed diff，低置信度只标记。
四、Keep list 防止误删
业务上下文、质量标准、工具契约、脆弱操作的精确顺序和仍能复现的限制都要保留。审计目标是找特定 dated pattern，不是比字符数。
五、中文入口如何适配
skills-zh 保留 219 行英文事实 reference 原样，中文入口新增两个真实场景：清理 Claude 3.5 时代客服 Prompt，以及迁移 Opus 5 后收尾 prefill、思维脚手架与工具描述。
触发评测增加 2 个正例和 1 个近似反例。纯翻译且要求结构不变时，不自行扩展为 Prompt 审计。
六、如何验证
运行 python3 scripts/validate_repository.py 检查 17 个本土化 Skill。
再运行 quick_validate 和 package_skill 验证 claude-api 入口与分发包。
本轮仓库门禁、打包、Python 和 Shell 语法、上游 reference 一致性以及平台 payload 全部通过。
仓库门禁只能证明同步完整。具体删除是否改善模型行为，还要在目标模型上做修改前后 probe。
项目地址：
https://github.com/MarcelLeon/skills-zh
