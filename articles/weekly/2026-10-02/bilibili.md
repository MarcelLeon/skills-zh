---
title: 调 Agent Prompt 前，先把 eval 做成闭环
tags: [Claude, Agent, Prompt工程, 测试]
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---
调 Agent Prompt 前，先把 eval 做成闭环
上游版本：8a1541c
本周范围：2 个提交，1 个 Skill，72 个文件
一、为什么成功截图不够
改完 Prompt 后挑几个回答截图，无法证明整体质量提升。
真正的 eval 至少有三部分：代表真实工作的输入、复用生产路径的 runner、能判断目标质量的 grader。
输入和评分方式都要让使用者确认。真实 API 全量运行前，还要先测单次成本并确认预算。
二、先审计 eval
eval-audit 检查 case、harness、metrics 和 grader。
它关注测试是否走真实工具链、指标是否掩盖严重失败、grader 是否泄漏答案，以及这套评测能不能测出准备比较的改动。
评测本身不可信，后面的优化只是在追逐噪声。
三、hillclimb 要隔离 test
train 用于找失败模式。
validation 用于选择方案。
test 保持独立，不能每轮看完再反向改 Prompt。
每轮记录唯一改动、三组分数、token、费用和停止条件。上游提供轻量 HTML report builder 和 runner scaffold，不需要临时写另一套看板。
四、5.5 模型迁移不是换字符串
上游示例默认更新为 Claude Opus 5.5，并加入 Claude Sonnet 5.5。
迁移还要检查 thinking 和 effort、forced tool use、平台可用性与 preserved-thinking 历史前缀。
启用 eager input streaming 后，大工具参数会边生成边到达，但客户端必须在执行工具前校验完整 JSON 和 schema。
五、验证边界
仓库 validator 通过 19 个中文 Skill。claude-api quick validate、打包和 ZIP、Python/Shell/Node 语法、17 个正例与 7 个反例路由、71 个事实文件内容一致性、诊断脚本 dry-run、报告生成和六平台 payload 均通过。上游文件另有 16 处纯空白归一化。
没有用户对付费预算的确认，因此不调用真实 Claude API，不运行全量 eval、hillclimb 或 preserved-thinking replay。
项目地址：
https://github.com/MarcelLeon/skills-zh
