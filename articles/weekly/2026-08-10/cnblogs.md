---
title: Managed Agents 进生产前，先把预算、数据驻留和多 Agent 边界说清楚
tags: [Claude API, Managed Agents, Agent Skills, 多 Agent]
categories: [AI]
links:
  - https://github.com/MarcelLeon/skills-zh
images: []
---

# Managed Agents 进生产前，先把预算、数据驻留和多 Agent 边界说清楚

Agent 能跑起来，不等于能放心交给生产环境。

当一个任务开始并行读很多材料、调用工具、运行几十分钟，真正影响上线决策的往往不是“再加一个模型”，而是三个更具体的问题：一次 session 最多能花多少；推理发生在哪个区域；多 Agent 到底怎么分工才不会把成本和上下文一起放大。

本周 skills-zh 对齐 Anthropic 上游提交 `f17010c`。这次 `claude-api` 的 18 个文件发生变化，上游净增 269 行，主角正是 Managed Agents 的预算、inference geo、仓库 Skills、Advisor 和 multiagent 编排。

## 一、Session budget 是硬上限，不是 token 提醒

Messages API 的 `task_budget` 是 token 维度的建议预算，帮助模型在一次 agent loop 中安排节奏。Managed Agents 的 session budget 不同：它按公开价追踪 session 的美元成本，并在达到上限后停止发起新的模型请求。

达到上限时 session 不会销毁，而是进入 idle，并给出 `stop_reason: budget_reached`。历史和 sandbox 仍在，但普通 `user.message` 不能让它继续；只有把预算改到高于已消耗成本，或移除预算，才能恢复。

这里还有一个容易踩坑的差异：session budget 只能在创建时加入，移除后不能重新加回；deployment budget 可以更新、清除和重新加入，并复制到之后每次调度创建的 session。

中文入口因此新增了一个真实任务：代码审查 Agent 每次最多花 25 美元，达到上限先暂停，审批后再继续。路由要求先区分 session budget 与 `task_budget`，再检查 `session.usage` 和事件顺序，避免把“提示模型省一点”误写成平台硬门禁。

## 二、数据驻留不是随手加一个顶层参数

Messages API 里的 `inference_geo` 是请求顶层参数；Managed Agents 则把它放在 agent 的 `model` 对象中。

它不只是创建时校验。上游 reference 明确写了：workspace 的允许区域发生变化后，原有 pin 不会被 grandfather；不再合规的运行中 session 后续 turn 也会被拒绝。对于 multiagent，coordinator 和所有 roster 成员还必须使用同一 geo，或者全部不设置。

因此中文 few-shot 没有只写“设置 US”，而是写成“主 Agent、worker 和 Advisor 如何一起满足 US inference”，把 roster 一致性和 Advisor 配对规则放进验收。

## 三、仓库里的 Skills 也是信任边界

Managed Agents 的 cloud sandbox 挂载 GitHub 仓库后，会在 session 启动时发现仓库根目录 `.claude/skills/<skill-name>/`。这让 Skill 可以和代码一起版本管理，不必每次单独上传。

便利背后有明确边界：只发现根目录下一层；只在 session 启动时扫描一次；self-hosted sandbox 不支持这一发现方式。更重要的是，Skill 是 Agent 指令。任何能把内容合入 `.claude/skills` 的人，都可能改变 Agent 在拥有 Bash、文件和网络工具时的行为。

所以本土化入口把“能不能自动加载”与“谁有权修改这些指令”放在同一个案例里，而不是把它写成一个纯路径功能。

## 四、多 Agent 从 self 开始，不要先堆角色

上游这次新增了一套很实用的顺序：

1. 任务能拆成独立部分时，先让 roster 只有 `self`，验证是否真的值得委派。
2. 把搜索、阅读、抽取等高输入、低推理任务交给更便宜的 worker。
3. 只有不同子任务确实需要不同工具和专业提示时，再加入 reviewer、test writer 等专门角色。

Advisor 是另一种能力。Managed Agents 通过 `{type: "advisor", model}` 的 roster 入口配置，建议通过 thread events 交给 primary thread；Messages API 的 Advisor tool 则有 `max_uses`、`max_tokens`、`caching` 等配置，两种接口不能混用。

## 五、我们如何同步，而不是重新制造一套事实

17 个英文事实性 reference 直接保持与上游一致。中文 `SKILL.md` 只负责三件事：什么时候应该触发；真实中文任务该读哪份 reference；哪些相邻概念不能混用。

本次新增了 3 个中文 few-shot、4 个应触发评测，并加入普通云预算、OpenAI/LangGraph 多 Agent 等近似反例。这样验证的不是“有没有翻译完”，而是中文用户不说 Skill 名时，入口能否把任务送到正确事实来源。

## 六、如何复现

```bash
python3 scripts/upstream_diff_report.py --base b29e7cf65e5cb78a5ac33d582270551bc74a14eb --head upstream/main
python3 scripts/validate_repository.py
python3 skills/skill-creator/scripts/quick_validate.py skills/claude-api
PYTHONPATH=skills/skill-creator python3 -m scripts.package_skill skills/claude-api /tmp/skill-dist
```

本次仓库校验通过 17 个本土化 Skill，`claude-api` 快速校验和打包通过，Python 与 Shell 语法检查通过，事实性 reference 与上游一致。

限制也要说清楚：这次上游是 Markdown/reference 更新，我们没有调用真实 Managed Agents beta API，所以没有把预算暂停、geo pin 和 Advisor 写成当前账号已线上实测。

项目地址：https://github.com/MarcelLeon/skills-zh
