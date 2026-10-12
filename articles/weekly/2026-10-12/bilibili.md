---
title: 超过25个子线程时，Managed Agents 怎么切动态工作流
tags: [Claude, ManagedAgents, AIAgent, 开发工具]
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---
超过25个子线程时，Managed Agents 怎么切动态工作流
上游版本：dbd4588
本周范围：2个提交，1个Skill，54个文件
一、不要把大任务硬塞进roster
Roster适合若干独立任务。
一项工作有数百个条目、必须分批才能避开25个child thread上限时，应该使用dynamic workflows。
服务端会按阶段运行workflow run，处理大量任务碎片。
二、开启能力还要写清使用条件
Agent配置使用multiagent_20261001并启用workflows。
System prompt必须说明哪些大任务启动run，哪些小任务自己完成，不能无条件总是启动。
每个Agent都会消耗token，所以session需要预算，也要告诉用户如何关闭。
用户明确不要时，使用roster-only coordinator或显式disabled。
三、单问单答不要过度编排
客服问答、文档Q&A、辅导解题等逐题任务默认由一个Agent自检。
不要自动给每个答案再加checker、voter、auditor或第二次模型调用。
一题本身需要拆很多独立文件，或用户明确接受checker成本时，再扩展编排。
四、四个新模板
Bug hunter按找候选、筛选、证明分阶段。
Explainer video按scene并行，再统一审查和修复。
Performance tuner逐函数优化、交叉检查、重做和统一测量。
Watchlist scanner逐ticker扫描，再逐ticker复核。
五、网页网络边界已修正
Limited allowed_hosts现在也限制web search和web fetch。
网页工具不用时默认关闭；需要时同时限制environment host和工具domain。
六、Haiku 5.5不是只换模型ID
还要处理adaptive thinking、sampling、assistant prefill、computer toolset、preserved thinking、refusal和100K输入价格分界。
七、本地证据与限制
中文入口新增3个真实场景、3个正例和1个近似反例，当前22个正例和9个反例。
仓库validator、quick validate、打包、ZIP、Python和Shell语法、13个quickstart结构smoke通过。
本机没有ant CLI和测试工作区，没有真实启动workflow run或调用Haiku 5.5。
项目地址：
https://github.com/MarcelLeon/skills-zh
