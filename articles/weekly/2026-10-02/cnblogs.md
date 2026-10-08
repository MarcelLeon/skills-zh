---
title: 别再挑成功案例：给 Claude 应用补一条可审计的 eval 闭环
tags: [Claude API, Eval, Agent, Prompt Engineering]
categories: [AI]
links:
  - https://github.com/MarcelLeon/skills-zh
images: []
---

# 别再挑成功案例：给 Claude 应用补一条可审计的 eval 闭环

改完 Agent 的 Prompt，最容易做的验收是挑几个看起来不错的回答截图。它很快，也几乎无法回答真正的问题：改动是整体更好，还是只对眼前样本更好？质量提升来自 Prompt，还是 grader、工具或测试集偷偷变了？

Anthropic Agent Skills 上游 `8a1541c` 新增了一组 eval/hillclimb 指南和执行资产。skills-zh 本轮没有逐句翻译英文入口，而是把它改造成中文开发者能自然触发的工作流：先建立可信 eval，再隔离 train/validation/test 做迭代，最后把质量、成本、失败样本和停止条件放在同一份证据里。

## 一、一个 eval 至少有三部分

这里的 eval 不是某个特定框架，而是：

1. 一组代表真实工作的输入；
2. 一个能按生产路径运行应用的 runner；
3. 一种能判断输出是否达标的 grader。

`shared/evals/build-eval.md` 要求先找到应用入口，读清模型、平台、Prompt、工具和输出形态，再决定样本从已有测试、脱敏真实记录还是合成边界案例中来。

关键门禁是：用户要认可输入确实代表关心的问题，也要认可 grader 测到的是正确目标。真实 API 全量运行前，还要先实测单次成本并确认预算。

## 二、先审计 eval，再用它调参

一个分数不等于一套可信评测。`shared/evals/eval-audit.md` 会检查：

- case 是否覆盖目标行为和失败边界；
- harness 是否真的走生产路径；
- grader 是否泄漏答案、偏爱格式或只测表面；
- 指标是否掩盖少量严重失败；
- 这套 eval 是否有能力区分准备比较的改动。

如果评测本身测不出目标变化，后面的优化只是在追逐噪声。

## 三、hillclimb 不是“每轮看 test 再改”

`shared/evals/eval-hillclimb.md` 把样本拆成 train、validation 和 test。train 用于发现问题与提出改动，validation 用于选择方案，test 保留为独立判断，不应变成下一轮 Prompt 的素材。

每轮至少记录：

- 只改了什么，什么明确没改；
- train/validation/test 分数；
- token、费用和运行时间；
- 新出现的失败样本；
- 是否达到停止条件。

上游还提供 report schema、轻量 HTML builder 与 runner scaffold。目标不是追求漂亮看板，而是让不同版本的结果能复现、能比较、能追责。

## 四、5.5 模型迁移仍然需要行为证据

同一轮上游把默认示例更新为 Claude Opus 5.5，并加入 Claude Sonnet 5.5。真正需要注意的不是字符串替换，而是 thinking/effort、forced tool use、Advisor 配对、task budget 和平台支持的差异。

例如旧项目显式关闭 thinking，迁移到新模型时不能沿用原假设；工具参数很大并启用 `eager_input_streaming` 时，客户端还要对累积 JSON 做 schema 校验，并在 `max_tokens` 或 `refusal` 时阻止工具执行。

这也是为什么模型迁移最好落到 eval，而不是“请求返回 200 就算完成”。

## 五、preserved thinking 要先测前缀变化

新的 `preserved-thinking-migration` 指南处理另一类隐蔽问题：应用在多轮会话中重写 system、tools 或历史消息，导致之前的 thinking block 不再属于当前前缀。

上游提供两份脚本：

```bash
python3 skills/claude-api/shared/preserved-thinking-migration/prefix_diff.py --help
python3 skills/claude-api/shared/preserved-thinking-migration/drop_block_probe.py --help
```

流程先捕获连续请求并做 prefix diff；真实 replay 前先 dry-run、估算输入成本并得到确认。结果按 conversation 统计“新失效的 thinking block”，不能把同一块在后续轮次反复失败算成多个问题。

## 六、如何复现本地验收

```bash
python3 scripts/validate_repository.py
python3 skills/skill-creator/scripts/quick_validate.py skills/claude-api
python3 -m compileall skills/claude-api
find skills/claude-api -name '*.sh' -exec bash -n {} +
```

本轮已核对 71 个事实性支撑文件：上游事实、命令与代码行为保持一致，仅 16 处行尾空格/末尾空行做仓库级纯空白归一化。仓库 validator 通过 19 个本土化 Skill；`claude-api` quick validate、打包/ZIP、Python/Shell/Node 语法、中文路由、preserved-thinking dry-run 与报告构建 smoke 均通过。六个平台 payload 无错误；小红书正文 525 字符、205 个中文字符，唯一警告是没有声明图片。

## 限制

本周实际上游范围是 `34040c9..8a1541c`：2 个提交、1 个 Skill、72 个文件、+6982/-620。本文证明的是上游内容同步、中文路由与本地确定性校验。

没有用户对付费预算的确认，本轮不会运行真实 Claude API、全量 eval、hillclimb 或 preserved-thinking replay，也不会把文档中的模型行为写成当前账号的生产验收结果。

项目地址：https://github.com/MarcelLeon/skills-zh
