---
title: skills-zh 发布说明：Managed Agents 生产治理能力更新
category: 人工智能
tags: [Claude, Agent, 多Agent, 开发工具]
summary: 用上游 diff 和仓库门禁梳理 Managed Agents 的硬预算、推理区域、仓库 Skills 与 Advisor 边界。
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

# skills-zh 发布说明：Managed Agents 生产治理能力更新

> 2026.08.10｜上游 `f17010c`｜`claude-api` 18 个文件｜Draft PR #1 CI Passed

Agent demo 常关注模型和工具，生产实现更容易栽在状态、成本与信任边界上。

skills-zh 本周对齐 Anthropic 上游 `f17010c`。这次只有 `claude-api` 变化，但涉及 18 个文件，核心是 Managed Agents 的 session/deployment budget、`inference_geo`、repository Skills、Advisor 和 multiagent 分工。

## 1. 两种 budget 不是一回事

Messages API 的 `task_budget` 是 token 型建议预算；Managed Agents session budget 是平台按公开价执行的美元硬上限。

达到上限时会出现 `budget_reached`。session 保留历史与 sandbox，但普通消息不能恢复它，必须修改或移除预算。Session budget 创建后可修改，移除后不能重新加入；deployment budget 则可以清除并重新加入，只影响之后触发的 session。

客户端不能只看数字轮询后发送 interrupt。更可靠的判断是消费 session 级 `stop_reason` 与紧邻的 `session.usage` 事件。

## 2. Managed Agents 的 geo 在 model 里

Messages API 把 `inference_geo` 放在请求顶层；Managed Agents 放在 `model` 对象中。Multiagent roster 的 coordinator、worker 和 Advisor 必须 geo 一致或全部不设。

这个 pin 也不是“创建后永久放行”。若 workspace allowlist 后续收紧，运行中 session 的后续 turn 也可能被拒绝。

## 3. `.claude/skills` 是代码，也是指令

cloud sandbox 挂载 GitHub 仓库后，会在 session 启动时发现根目录 `.claude/skills/<skill-name>/`。只扫描根目录下一层，而且只扫描一次。

这让 Skill 能跟代码一起版本化，也把仓库写权限变成了 Agent 指令权限。外部 PR、依赖或贡献者一旦能修改该目录，就可能影响拥有 Bash、文件和网络工具的 Agent。挂载前审计不能省。

## 4. Multiagent 从 self 和便宜 worker 开始

适合 multiagent 的任务通常能拆成独立阅读或处理单元。先只配置 `self`，确认委派能降低主上下文压力；再把检索、阅读、抽取交给便宜 worker；只有确有不同工具或专业边界时再增加 reviewer、test writer 等角色。

Advisor 不是普通 roster agent。Managed Agents 用 `{type: "advisor", model}`，建议通过 thread events 交给 primary thread；Messages API 的 Advisor tool 是另一套参数和结果结构。

## 本土化怎么验收

这次没有把上游英文入口覆盖到中文文件：17 个事实性 reference 保持原样，中文入口新增 3 个真实 few-shot，并把 `claude-api` 触发评测扩展到预算、US inference、仓库 Skills 与低成本 worker。同时加入普通云预算、OpenAI/LangGraph 多 Agent 的近似反例。

复现命令：

```bash
python3 scripts/validate_repository.py
python3 skills/skill-creator/scripts/quick_validate.py skills/claude-api
PYTHONPATH=skills/skill-creator python3 -m scripts.package_skill skills/claude-api /tmp/skill-dist
```

本次 17 个本土化 Skill 的仓库门禁通过，`claude-api` 校验和打包通过，Python/Shell 语法检查通过。没有调用真实 Managed Agents beta API，因此线上预算与 geo 行为仍保留为待账号环境验证的边界。

项目：https://github.com/MarcelLeon/skills-zh
