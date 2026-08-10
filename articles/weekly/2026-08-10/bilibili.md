---
title: Managed Agents 进生产前：预算、驻留与多 Agent 边界
tags: [Claude, Agent, 多Agent, 开发工具]
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---
一、Agent 能跑不等于能进生产
本周 skills-zh 对齐 Anthropic 上游 f17010c。claude-api 共 18 个文件变化，重点不是新模型，而是 Managed Agents 的预算、推理区域、仓库 Skills、Advisor 和多 Agent 分工。
二、美元硬预算不是 token 提醒
Messages API 的 task_budget 是 token 型建议预算。Managed Agents 的 session budget 是平台执行的美元硬上限。
达到 budget_reached 后，session 保留历史和 sandbox，但普通消息不能让它继续。只有修改或移除预算才能恢复。
Session budget 移除后不能重新加入。Deployment budget 可以清除后再加入，并复制到后续每次触发的 session。
三、数据驻留要检查整个 roster
Managed Agents 的 inference_geo 写在 model 对象里。Coordinator、worker 和 Advisor 必须使用同一 geo，或者全部不设置。
Workspace 的允许区域后来收紧时，旧 session 也不会自动获得豁免。
四、仓库 Skills 是信任边界
Cloud sandbox 挂载 GitHub 仓库后，会在 session 启动时发现根目录 .claude/skills 下的一层 Skill。
它只扫描一次。能修改这个目录的人，也能修改 Agent 指令。挂载外部贡献者仓库前必须审计。
五、多 Agent 从最小 roster 开始
先用 self 验证任务是否值得委派，再把搜索、阅读、抽取交给便宜 worker。只有不同任务确实需要不同工具和提示时，才增加 reviewer 或 test writer。
Advisor 通过专用 roster 入口配置，结果从 thread events 交付，不能和 Messages API 的 Advisor tool 参数混用。
六、中文本土化如何验收
事实性 reference 与上游保持一致。中文入口增加 3 个真实 few-shot，并加入预算、US inference、仓库 Skills 和低成本 worker 的触发案例，以及普通云预算、OpenAI 和 LangGraph 的近似反例。
运行 python3 scripts/validate_repository.py 可检查全部 17 个本土化 Skill。
本次仓库校验、Skill 打包、Python 和 Shell 语法检查都通过。没有调用真实 Managed Agents beta API，所以线上行为仍明确标记为未实测。
项目地址：
https://github.com/MarcelLeon/skills-zh
