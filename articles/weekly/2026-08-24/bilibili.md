---
title: Anthropic Python SDK 1.x 升级：先找边界，再改代码
tags: [Claude, Python, SDK升级, Agent]
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---
Anthropic Python SDK 1.x 升级：先找边界，再改代码
上游版本：3b3fad9
影响范围：新增两个 Skill，更新 claude-api，共 9 个文件
一、为什么不能只改版本号
大版本升级最危险的情况不是安装失败，而是能装、能 import、局部测试也通过，但 HTTP mock、异步 response、旧接口或部署默认值已经悄悄失效。
skills-zh 本周为 claude-api 接入 upgrade 路由，当前覆盖 Python anthropic SDK 0.x 到 1.x。
二、先确认范围和真实目标版本
upgrade python 没带路径时，先确认整个工作目录、某个子目录或明确文件。
代码进入范围后，根目录依赖清单、lockfile、CI 和 Python floor 也要检查。
2026 年 8 月 24 日的实际查询确认 anthropic 1.0.0 已发布。一次性 Python 3.11 环境安装后，包元数据要求 Python 大于等于 3.10，并安装 httpx2 2.12.0。
三、Inventory 避免全局误改
先搜索 Python 3.9 声明、import httpx、with_raw_response、Text Completions、sampling 参数、output_format、parse stream、client-side compaction 和 Bedrock client。
每个命中都要分成 SDK call site、无关同名代码、测试或范围内文档。其他服务自己的 httpx 请求不应被 Anthropic SDK 升级误伤。
四、必改项和用户决策分开
必改项包括 SDK 边界上的 httpx 对象切到 httpx2、async raw response 读取加 await、Text Completions 迁到 Messages，以及 removed 类型和参数。
用户决策包括 Python 3.10 floor、局部 import 还是进程级 alias、旧 sampling 参数是否承载业务语义、替换哪个模型、Bedrock region 是什么。
Agent 可以提供证据和修改建议，不能为了让测试通过就替用户猜部署地区。
五、验证要重跑同一份清单
迁移完成后重跑 inventory，每个残余命中都要有保留理由。然后运行 compileall、项目已有的类型检查和不需要真实凭据的测试。
本轮仓库验证通过 19 个中文 Skill、三个分发包、Python 和 Shell 语法、上游事实文件一致性，以及 anthropic 1.0.0 的隔离安装和 import。
没有拿真实 0.x 项目执行端到端升级，也没有调用 Claude API，所以不能宣称所有项目兼容。
六、另外两个新 Skill
academy-guide 只在用户真想学习 Claude 产品时推荐实时 Academy 内容。用户正在让 Agent 做任务时保持安静，目录取不到也不能凭记忆编造课程。
discernment-nudge 只在可行动的实质答案后追加一次两到三个具体问题。用户已经要求查证、纯教学、代码、创作和格式转换都跳过。
七、中文本土化如何验收
三个变化 Skill 都加入真实中文 few-shot，以及至少两个正例和一个相邻反例。
确定性 smoke 能证明入口、边界和分发包完整，但不等于模型触发率已经在线实测。
项目地址：
https://github.com/MarcelLeon/skills-zh
