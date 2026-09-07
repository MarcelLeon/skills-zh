---
title: Claude API 降本，先别急着换便宜模型
tags: [Claude API, 成本优化, Agent, Agent Skills]
categories: [AI]
links:
  - https://github.com/MarcelLeon/skills-zh
images: []
---

# Claude API 降本，先别急着换便宜模型

“账单涨了，换个便宜模型吧”是 LLM 应用里很自然的反应，也常常是最早下手、最难归因的一步。

本周 skills-zh 对齐 Anthropic Agent Skills 上游 `41bbe19`。`claude-api` 新增的核心能力不是一张价格表，而是一条 `cost-optimize` 工作流：先确认优化范围、质量门槛和当前成本，再找 token 花在哪里；先处理不该付的钱，最后才讨论需要牺牲什么。

同一轮还加入组织 Admin API 参考、Fable/Mythos 5.1 的迁移事实，并更新 `frontend-design` 的反模板规则。它们共同强调一件事：Agent 可以把证据和选项组织好，但不能把付费、权限或质量取舍藏在自动化里。

## 一、成本基线有三层证据

最好的输入是 Usage/Cost Admin API。它能提供真实用量和金额，但“每完成一项任务多少钱”的分母仍要来自应用日志或业务计数。

没有 Admin API key 时，先问应用是否已经保存 `response.usage`。regular input、cache write、cache read 与 output 的价格权重不同，不能只把 token 总数相加。

两种数据都没有时，才从请求构造代码估算：稳定 system/tools 前缀有多大，用户载荷有多大，工具结果是否不断回灌，Agent 平均跑多少轮，输出是否经常顶到上限。估算必须标明误差，不能写成“已节省 30%”。

## 二、先做 free wins，再做质量 tradeoff

工作流建议先检查：

1. Prompt Caching 是否真的命中，动态内容是否误放在稳定前缀里；
2. 大参考资料能否按需加载，而不是每次全量塞进上下文；
3. 长 Agent 循环是否重复回放大段工具结果；
4. 输出是否有明确形状和停止条件；
5. 无人等待的独立任务能否使用 Batch。

这些候选项之后，才轮到降低 effort、收紧预算、切换模型或建立多模型路由。原因不是保守，而是后四项会直接改变质量；如果没有冻结样本和结果检查，账单可能下降，但重试次数、失败率或人工复核时间会把“节省”吃回去。

一个可复现的仓库验收命令是：

```bash
python3 scripts/validate_repository.py
```

本轮结果为 `Repository validation passed: 19 localized skills`。`claude-api` 与 `frontend-design` 还分别通过 quick validate、打包与 ZIP 完整性检查。

## 三、每个 lever 单独成 diff

如果同时改缓存、裁剪工具结果、降低 effort 并换模型，最后几乎无法回答“究竟哪一步省了多少钱、哪一步伤了质量”。

新的中文路由要求每个 lever 单独提出、单独测量、单独保留或回滚。真实模型评测会花钱，因此先列出固定样本、配置数量、判断方法和预计预算，拿到确认后再运行。没有质量检查时，free win 可以作为成本测量方案，tradeoff 只保留为提案。

## 四、Admin API 的权限边界不能混

新增的 `shared/admin-api.md` 覆盖成员、邀请、工作区、API key、rate limit、服务账号、WIF 与 CMEK。最容易混淆的是凭据：Messages API key 用来调用模型，Admin API key 管理大多数组织资源，而服务账号/WIF 等端点要求 `org:admin` OAuth。

自动化脚本应该先给最小权限和只读/dry-run 方案。成员移除、角色修改、key 停用等都是外部写操作，不能因为 API 存在就默认执行。

## 五、Fable 5.1 迁移也不只是换 ID

上游 reference 新增 Fable/Mythos 5.1 的完整迁移面。进入这条路由后，需要检查 forced tool use、thinking block 的模型绑定、历史消息是否 append-only、`stop_reason: refusal`、fallback、数据保留、长请求的 streaming/timeout 以及目标平台支持矩阵。

这些事实变化快。skills-zh 的中文入口负责把问题路由到正确 reference，不复制一份很快过期的“当前模型大全”。当用户问“现在支持什么”时，仍应以 Models API 或官方实时来源为准。

## 六、前端反模板也要能验收

`frontend-design` 这次把一些高频通用默认写成检查项：同款圆角卡片套一切、全大写眉题、单词变色、小号等宽标签、按钮末尾箭头，以及每段淡入上滑。它们不是禁用词，而是提醒设计者回答：这个选择是否真的来自当前主题？

中文本土化还补了投研看板和品牌故事页两个场景，明确一个字体家族也可以；使用两个时角色要明显不同，并检查中文长标题、可读行长、移动端与键盘焦点。

## 限制

本轮同步覆盖 2 个上游提交、2 个 Skill、70 个文件，仓库与分发包验证通过。但我们没有调用真实 Claude API，没有读取组织账单，没有执行 Admin API 写操作，也没有跑 Fable/Mythos 5.1 的运行时行为测试。因此文章描述的是已同步的官方参考与本地确定性验收，不是线上节省比例或端到端兼容性承诺。

项目地址：https://github.com/MarcelLeon/skills-zh
