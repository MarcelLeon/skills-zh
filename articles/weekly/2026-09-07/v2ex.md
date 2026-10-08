---
title: LLM 降本时，你们会先改缓存，还是先换模型？
node: programmer
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

最近同步 Anthropic Agent Skills 的 `claude-api`，上游新增了一套 `cost-optimize` 流程。我觉得比较值得讨论的是它没有从模型价格表开始，而是从 token profile 开始。

证据分三层：有 Admin API key 就读 Usage/Cost 报表；没有则先问应用有没有保存 `response.usage`；再没有才从请求构造、上下文和 Agent 轮数估算。金额可以来自报表，但“每完成一项任务多少钱”的分母还得来自业务或应用日志。

应用顺序也有意拆开：

1. Prompt Caching；
2. 按需加载参考资料、裁剪输入；
3. 控制长循环里重复回放的工具结果；
4. 约束输出；
5. 无人等待时用 Batch；
6. 最后才降低 effort、收紧预算、换模型或做多模型路由。

每个 lever 单独成 diff，用同一批请求测量后再保留或回滚。真实模型评测会花钱，所以先报样本、配置和预算，确认后才跑。没有质量检查时，tradeoff 只留提案。

这轮还新增 Admin API 参考，明确 Messages key、Admin key 和 `org:admin` OAuth 不是一回事；同时把 Fable/Mythos 5.1 的 forced tool use、thinking 回放、append-only history 和 refusal fallback 加进迁移路由。

另一个变化是 `frontend-design`：把统一圆角卡片、全大写眉题、单词变色、每段淡入上滑等“AI 页面高频默认”列成审查项。不是绝对禁用，而是要求说明为什么适合当前主题。

本地确定性验证已过：19 个 Skill 的仓库 validator、两个 Skill 的打包/ZIP、Python/Shell 语法、路由 smoke 和上游事实文件一致性。没有读真实账单，也没有调用模型，所以没有节省比例结论。

大家线上做 LLM cost optimization 时，更有效的第一步通常是什么？你们能把 cost per request 进一步归因到 cost per completed task 吗？

项目：https://github.com/MarcelLeon/skills-zh
