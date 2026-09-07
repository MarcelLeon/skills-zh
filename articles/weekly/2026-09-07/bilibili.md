---
title: Claude API 降本：先找 token 去向，再谈换模型
tags: [Claude, Agent, 成本优化, 开发工具]
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---
Claude API 降本：先找 token 去向，再谈换模型
上游版本：41bbe19
本周范围：2 个提交，2 个 Skill，70 个文件
一、为什么不能先换便宜模型
如果不知道成本来自稳定前缀、用户输入、工具结果、长循环还是输出，直接换模型会把成本和质量两个变量混在一起。
skills-zh 本周给 claude-api 加入 cost-optimize 中文路由，第一步是确认范围、质量门槛和基线。
二、成本证据分三层
有 Admin API key 时读 Usage 和 Cost 报表。
没有时先看应用是否保存 response.usage，按完成任务汇总 input、cache write、cache read 和 output。
再没有才从代码估算，并明确误差。
三、先做 free wins
先检查 Prompt Caching、按需加载参考资料、长循环工具结果裁剪、输出约束和 Batch。
之后才降低 effort、收紧预算、切模型或做多模型路由，因为这些会改变质量。
每个 lever 单独成 diff。真实模型评测会花钱，先列样本、配置和预计预算，取得确认后再运行。
四、Admin API 的凭据不能混用
新增参考覆盖组织成员、workspace、API key、rate limit、服务账号、WIF 和 CMEK。
Messages API key、Admin API key 与 org:admin OAuth 权限不同。服务账号和 WIF 等 OAuth-only 端点不能拿 admin key 试错。
五、Fable 5.1 迁移不是换 ID
迁移时还要检查 forced tool use、append-only history、thinking block 回放、stop_reason refusal、fallback、数据保留和目标平台支持。
六、前端设计新增反模板审查
frontend-design 把同款圆角卡片、全大写眉题、单词变色、小号等宽标签和每段淡入上滑列成检查项。
这些风格不是绝对禁止，但必须能解释为什么服务当前主题和用户任务。
七、验证与边界
仓库 validator 通过 19 个本土化 Skill。两个变化 Skill 的 quick validate、分发包和 ZIP 完整性通过；Python 和 Shell 语法、中文路由 smoke、事实文件一致性也通过。
本轮没有调用真实 Claude API，没有读取组织账单，没有执行 Admin API 写操作，也没有做模型级触发 A/B。
项目地址：
https://github.com/MarcelLeon/skills-zh
