---
title: 从 httpx2 到 Bedrock region：把 Anthropic SDK 1.x 升级做成可验证流程
category: 人工智能
tags: [Claude, Python, SDK, Agent]
summary: 用范围确认、inventory、BREAKS/DECIDE 和验证报告拆解 Anthropic Python SDK 0.x 到 1.x 升级。
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

# 从 httpx2 到 Bedrock region：把 Anthropic SDK 1.x 升级做成可验证流程

大版本升级不应该从“把依赖改成 1.0”开始，而应该从“这次到底允许改哪里”开始。

skills-zh 本周对齐 Anthropic Agent Skills `3b3fad9`，为 `claude-api` 新增 `upgrade` 路由。当前内置的是 Python `anthropic` SDK 0.x→1.x：一份 286 行的执行指南，不只列 breaking changes，还要求把范围、命中、用户决策、验证结果和未验证项一起交付。

## 第一步不是编辑，是定范围和版本

`upgrade python` 没带路径时，需要先让用户选择整个工作目录、子目录或明确文件。代码进入范围后，根目录依赖文件和 lockfile 也要检查。

写精确 pin 前还要验证 1.x 已发布。2026-08-24 的实际查询返回 `anthropic 1.0.0`；一次性 Python 3.11 环境安装后确认：

- `Requires-Python >=3.10`；
- SDK 安装 `httpx2 2.12.0`；
- `anthropic.Timeout` 可正常构造；
- `pip check` 无依赖冲突。

## Inventory 让迁移不靠猜

指南先搜索 Python 3.9 声明、`import httpx`、`with_raw_response`、Text Completions、sampling 参数、raw `output_format`、`parse(stream=)`、client-side compaction、Bedrock client 等信号。

每个命中再分类为 SDK 调用、无关同名变量、测试或范围内文档。比如项目给其他服务发 `httpx` 请求，不应因为 Anthropic SDK 换 HTTP 层就全仓替换。

## `[BREAKS]` 与 `[DECIDE]` 要分开

必改项包括：

- SDK 边界上的 `httpx` 对象切到 `httpx2`；
- async raw response 的 `parse/json/text/read` 加 `await`；
- Text Completions 迁到 Messages；
- removed 类型、参数和 helper 行为改到新接口。

用户决策包括：

- 是否把 Python floor 和 CI matrix 提到 3.10；
- 应用用局部 `httpx2` import，还是进程级 `alias_httpx()`；
- 旧采样参数是否仍有业务依赖；
- 旧 Completions 代码换哪个在服模型；
- Bedrock region 和 invocation metrics 如何处理。

Agent 可以给证据和 proposed hunk，不能为了让测试绿就替用户决定部署地区。

## 验证要回到搜索清单

迁移完成后重跑 inventory，每个残余命中都要解释，再执行 compileall、项目已有的 pyright/mypy 和可运行测试。没有网络、凭据或 type checker 时，要把精确补跑命令写进报告。

本轮同步验证了 19 个中文 Skill、三个分发包、Python/Shell 语法、upstream reference 一致性和 1.0.0 隔离安装。没有拿真实 0.x 项目跑 end-to-end upgrade，也没有调用 Claude API，所以不会把“指南已打包”写成“所有项目兼容”。

## 两个新 Skill 也在处理边界

`academy-guide` 只在用户真正想学 Claude 产品时推荐实时 Academy 内容；执行任务中途不打扰，目录不可用就不编造具体课程。

`discernment-nudge` 只在用户可能据此行动的实质答案后追加一次 2–3 个具体问题；用户已要求核验、纯教学、代码、创作或格式化时都跳过。

中文本土化为每个变化 Skill 增加两个真实 few-shot，以及至少两个正例和一个近似反例。这里验证的是路由契约完整，不是宣称模型触发率 100%。

复现仓库门禁：

```bash
python3 scripts/validate_repository.py
python3 skills/skill-creator/scripts/quick_validate.py skills/claude-api
```

项目：https://github.com/MarcelLeon/skills-zh
