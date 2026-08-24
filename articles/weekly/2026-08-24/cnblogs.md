---
title: Anthropic Python SDK 1.x 升级，不只是把版本号改成 1.0
tags: [Claude API, Python, SDK升级, Agent Skills]
categories: [AI]
links:
  - https://github.com/MarcelLeon/skills-zh
images: []
---

# Anthropic Python SDK 1.x 升级，不只是把版本号改成 1.0

大版本升级最危险的时刻，通常不是安装失败，而是“能装、能 import、局部测试也绿”，但一些边界行为已经悄悄换了。

本周 skills-zh 对齐 Anthropic Agent Skills 上游 `3b3fad9`，为 `claude-api` 加入 Python `anthropic` SDK 0.x→1.x 的 `upgrade` 流程。它不是一页 breaking changes 摘要，而是一条可以落到仓库里的执行链：先定范围，再盘点命中，区分必改项和用户决策，最后重跑搜索、类型检查和测试。

同一批上游变化还新增了 `academy-guide` 与 `discernment-nudge`。一个约束学习资源推荐不要打扰执行中任务，另一个约束 AI 在可行动答案后只做一次具体提醒。三者看似不同，其实都在解决同一件事：Agent 不只要“知道内容”，还要知道什么时候执行、什么时候停、哪些决定不能替用户做。

## 一、先确认升级对象，而不是先改版本号

`/claude-api upgrade python` 本身仍然是一个范围不明的请求。升级流程要求先确认：

- 整个工作目录；
- 某个子目录；
- 一组明确文件。

只要代码进入范围，项目根目录里的 `pyproject.toml`、`requirements*.txt`、`uv.lock`、`poetry.lock` 等依赖与锁文件也随之进入检查面。这样可以避免只改调用代码，却漏掉 CI、Docker、Python floor 或 lockfile。

接着读取声明版本和已安装版本，并在写 pin 前确认 1.x 真的已经发布。2026-08-24 的验证中，`pip index versions anthropic` 返回最新版本 `1.0.0`；一次性 Python 3.11 环境成功安装后，包元数据显示 `Requires-Python >=3.10`，并安装 `httpx2 2.12.0`。

这条 live check 很重要。离线时可以先写 `anthropic>=1,<2` 并明确“pin 未验证”，但不能凭上游文档猜一个不存在的精确版本。

## 二、Inventory 的价值是防止误改

指南把迁移信号组织成可搜索清单，包括：

- Python 3.9 声明和 CI matrix；
- `anthropic`、`httpx-aiohttp`、`import httpx`；
- `with_raw_response` 与 `LegacyAPIResponse`；
- `completions.create`、`HUMAN_PROMPT`、`AI_PROMPT`；
- `temperature`、`top_p`、`top_k`、`output_format`；
- `parse(stream=)`、`compaction_control`、raw bytes `body=`；
- Bedrock client 与 region 配置。

命中后仍要分类：SDK call site 才修改；同名的普通业务变量、其他服务的 `httpx` 请求、`urllib.parse`、温度传感器字段都应保留。测试、文档和 notebook 在范围内则一起改，避免示例继续教旧写法。

这比“全局替换 import”多一步，却能显著降低误伤。

## 三、`httpx2` 只在 SDK 边界上改变

1.x 的 HTTP 层切换到 `httpx2`。不是仓库里所有 `httpx` 都要替换，真正需要动的是交给 SDK 或从 SDK 返回的对象：

- `Timeout`、`Limits`、transport、custom client；
- event hook 中的 request/response 类型；
- `APIStatusError.response`、`APIConnectionError.request`；
- raw/streaming response 的 HTTP 对象和类型判断。

如果某个模块只用 `httpx` 服务 Anthropic SDK，可以写 `import httpx2 as httpx`。如果同一模块还请求其他服务，就同时保留两个 import，只迁 SDK 边界。

应用还可以选择尽早调用 `httpx2.alias_httpx()`，让 tracing、APM、`respx`、`pytest-httpx` 等仍能观察 SDK 流量；但它必须发生在任何 `httpx/httpcore` import 之前，而且不能被库偷偷加进用户进程。这是典型的 `[DECIDE]`，不是 Agent 可以替所有项目做出的默认选择。

## 四、几个“看起来小”的 breaking changes

### Async raw response

async client 的 `parse()`、`json()`、`text()`、`read()` 变成需要 `await` 的 coroutine。sync client 的 `.text` 也变成 `.text()`，`.content` 变成 `.read()`。迁移必须沿着 `with_raw_response` 的值追踪，不能把项目里所有同名方法都加上 `await`。

### Text Completions

`client.completions.create()`、`HUMAN_PROMPT`、`AI_PROMPT` 被移除，需要迁到 Messages API。旧代码通常还绑着退休模型，所以这里同时出现一个用户决策：换哪个仍在服务的模型，以及旧 Prompt 是否需要 `prompt-audit`，不能只把 request shape 改到能运行。

### Sampling 与 structured output

`temperature`、`top_p`、`top_k` 从 1.x SDK 签名移除，但某些旧模型的 API 层仍可能接受。真正依赖采样参数的调用可在明确模型支持时放进 `extra_body`，否则删除；raw dict 型 `output_format` 要迁到 `output_config.format`，Pydantic class 型 `output_format=Model` 则保留。

### Bedrock region

`AnthropicBedrock()` 不再只警告后回退到 `us-east-1`。如果仓库不能证明部署提供了 `AWS_REGION`、`AWS_DEFAULT_REGION`、profile 或显式参数，就应该把 region 列成待确认事项，而不是为“让测试过”硬编码一个地区。

## 五、验证不是一句“测试通过”

`upgrade` 要求最后重跑 inventory。每个残余命中都要有理由，然后执行：

```bash
python -m compileall -q <scope>
# 若项目配置了 pyright / mypy，再运行对应类型检查
# 运行不需要真实凭据即可完成的测试
```

本轮同步自身使用 Python 3.11.14 隔离环境完成：

- 19 个本土化 Skill 的仓库 validator；
- `academy-guide`、`discernment-nudge`、`claude-api` quick validate；
- 三个 `.skill` 打包与 ZIP 完整性；
- Python compileall 与全仓 Skill Shell `bash -n`；
- 新增 LICENSE 与 `claude-api` 事实 reference 的 upstream blob 一致性；
- `anthropic 1.0.0` / `httpx2 2.12.0` 隔离 import 和依赖检查。

这些证据证明同步包完整、路由存在、官方 reference 未被本土化改坏，也证明 1.0.0 可以在 Python 3.11 环境安装。它们不能证明任意真实 0.x 项目都已经迁移成功；本轮没有对一个带旧 HTTP mock、APM 和 Bedrock 部署的样例仓库跑 end-to-end upgrade。

## 六、两个新 Skill 的本土化，不靠关键词堆叠

`academy-guide` 的中文 description 同时覆盖“怎么用、从哪开始、有没有教程、团队培训”和 Projects、Artifacts、Skills、MCP 等中英混输表达，但把“我正在让你做任务”列为反例。它必须先回答问题，再从实时 catalog 选强匹配项，最多两条；目录取不到就只给官方产品中心或资源库。

`discernment-nudge` 只针对用户会据此行动的建议、计划、估算、数据解释和关键草稿。若用户已经要求引用和核验，正文就该直接做完核验，不能再用“请自行检查”收尾。纯教学、代码、创作和格式转换也不触发。

中文触发评测为三个受影响 Skill 都补了至少 2 个正例和 1 个相邻反例。确定性 smoke 证明评测结构与边界完整，但没有把它包装成模型命中率：真正的 trigger A/B 仍需独立模型运行。

## 七、剩余限制

Claude Academy 官方站点可访问，但当前 CLI 直取 `assets/data/catalog.json` 两次超时，因此本轮没有验证 `staleAfter`、目录 schema 或具体 item 推荐。按照 Skill 自己的规则，这种情况只能降级，不能从记忆中编造课程标题和 URL。

文章包也只完成本地 payload 验证。没有平台真实预览、远程草稿或公开发布；所有外部动作仍要先确认账号、标题、正文、标签、图片和发布模式。

项目地址：

https://github.com/MarcelLeon/skills-zh
