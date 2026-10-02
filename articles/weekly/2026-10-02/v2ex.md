---
title: 你们调 Agent Prompt 时，test 集会每轮都看吗？
node: programmer
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

最近同步 Anthropic Agent Skills 的 `claude-api`，上游新增了一套 build-eval / eval-audit / hillclimb 指南。对我最有用的不是又多了一个评测框架，而是把几条容易被忽略的边界写死了。

一套 eval 至少有真实输入、复用生产路径的 runner、能测目标质量的 grader。先审计 case/harness/metrics/grader 是否真能区分目标改动，再谈优化。

hillclimb 使用 train/validation/test：train 找失败模式，validation 选方案，test 保持独立。每轮记录唯一改动、三组分数、token/费用与停止条件。如果每轮看完 test 再改 Prompt，test 其实已经变成 train。

这一轮还加入 Claude Opus 5.5 / Sonnet 5.5、preserved-thinking migration 与 `eager_input_streaming`。后两者也很适合放进 eval：历史消息前缀被应用重写时，thinking block 可能失效；大参数工具边流式生成边到达时，客户端必须在执行副作用前校验完整 JSON 和 schema。

skills-zh 的中文入口新增了三组场景：脱敏工单建 eval、5.5 模型迁移、TypeScript 大工具参数流式校验。71 个事实性支撑文件保持上游内容，本地再做 validator、语法、打包、路由和 parity。

本轮没有付费预算确认，所以不会运行真实 Claude API、全量 hillclimb 或 replay。能证明的是同步和本地确定性验收，不是线上质量提升。

大家的实践里，test 集多久看一次？如果业务样本很少，你们会保留多少做最终 test，怎样避免 grader 和 Prompt 一起过拟合？

项目：https://github.com/MarcelLeon/skills-zh
