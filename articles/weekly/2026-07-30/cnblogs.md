---
title: 我没有继续翻译 Skills，而是给中文 Agent 做了一套本土化验收
tags: [AI Agent, Agent Skills, Claude, 开源]
categories: [AI]
links:
  - https://github.com/MarcelLeon/skills-zh
images: []
---

# 我没有继续翻译 Skills，而是给中文 Agent 做了一套本土化验收

很多“中文 Skills 仓库”的同步方式只有两步：拉取英文版本，然后逐段翻译。这样得到的文档能读，但不一定好用。

真正影响 Skill 效果的，首先是模型会不会在真实任务里想起它。中文用户很少说“请调用 docx skill”，更常见的是：

> 把这份会议纪要整理成带目录和页码的正式 Word。

或者：

> 下载目录里那个销售台账，帮我补毛利率公式和区域汇总。

如果 description 只翻译了英文文件类型，口语、隐含交付物和相邻任务边界仍然缺失。

## 这次改造了什么

skills-zh 本次审计到 Anthropic 上游 `b29e7cf`，从 16 个 Skill 扩展到 17 个，新增 `claude-api`。

但重点不是数字，而是三项能力变化。

第一，DOCX、PPTX、XLSX 同步了 7 月新版脚本。新版增强了模板格式、压缩包输入安全、Office 关系和 schema 校验，也重构了共享 helper。对文档类 Agent 来说，这些比“多翻译几段说明”更重要，因为错误可能直接表现为文件损坏、修订丢失或公式不可用。

第二，`claude-api` 没有把数十份快速变化的 API reference 全部机器翻译。官方技术事实保留为可追溯参考，中文入口负责判断供应商、识别项目语言，并把“Java 流式接入”“Prompt Caching 不命中”“每天运行带工作区的 Agent”等任务路由到正确资料。

第三，项目新增了中文本土化契约和触发评测集。17 个 Skill 每个至少有两个应触发案例和一个相邻反例，共 51 条真实中文提示。

## 本土化不等于堆中文关键词

本次定义了四层适配：

1. 触发适配：正式说法、口语、中文文件名和隐含意图。
2. 场景适配：周报、方案评审、合同修订、数据台账等真实工作。
3. few-shot 适配：中文输入、明确产物、可检查结果。
4. 表达适配：正文以中文为主，API、命令和技术术语保持准确。

还要有反例。例如“把会议纪要润色一下，直接返回 Markdown”不应触发 DOCX；“只修按钮请求 bug，不要改样式”不应触发 frontend-design。

## 如何验证

仓库现在可以运行：

```bash
python3 scripts/validate_repository.py
```

它不只检查 YAML，还会检查：

- Skill 目录与 frontmatter 名称一致；
- 中文 description 和中文入口存在；
- marketplace 没有漏掉 Skill；
- 17 个 Skill 都有中文正反触发案例；
- 上游同步基线完整；
- README 不再引用已删除脚本。

本次验证结果是 17 个 Skill 全部通过。Python 3.11 语法和 Shell 语法检查也通过；最小 DOCX、PPTX 产物通过新版 validator。

限制也必须说清楚：XLSX 的 LibreOffice 公式回算在当前 macOS 环境连续超时，缓存值没有生成。因此目前只能确认脚本同步和语法正确，不能宣称回算链路已经实测通过。

## 下一步：把同步变成每周闭环

后续每周任务会：

1. 拉取 Anthropic 最新 main。
2. 先看安全和行为差异，不盲目覆盖中文入口。
3. 重写中文触发、场景、few-shot 和反例。
4. 运行仓库级门禁和受影响脚本 smoke test。
5. 生成技术文章包，重点解释本次新增核心能力。

公开文章仍保留人工预览确认。自动化可以生成可靠草稿，但不应在没有检查标题、格式、链接和事实的情况下替人点击发布。

项目地址：https://github.com/MarcelLeon/skills-zh
