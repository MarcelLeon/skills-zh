---
title: 从“中文翻译”到“中文触发验收”：我如何维护 17 个 Agent Skills
category: 人工智能
tags: [AI, Agent, Claude, 开源]
summary: 不再逐句翻译 Skill，而是同步上游能力，并用中文触发、few-shot、反例和仓库门禁验收。
links: [https://github.com/MarcelLeon/skills-zh]
images: []
---

# 从“中文翻译”到“中文触发验收”

Skill 是否好用，不只取决于说明有没有翻译。更关键的问题是：中文用户自然描述任务时，模型能否选中正确 Skill。

比如用户通常不会说“调用 xlsx skill”，而会说：

> 下载目录里的销售台账，补毛利率公式，再按区域汇总。

本次 skills-zh 对齐 Anthropic 上游 `b29e7cf`，新增 `claude-api`，并同步 DOCX/PPTX/XLSX 的 7 月安全与校验更新。

## 本土化的四层门禁

1. description 覆盖中文口语、隐含产物和中英混输。
2. 场景使用中文开发和办公中的真实任务。
3. few-shot 给出输入、执行路径和可检查结果。
4. 每个 Skill 同时维护近似但不应触发的反例。

当前 17 个 Skill 一共维护了 51 条中文正反触发案例。

## 仓库级验证

```bash
python3 scripts/validate_repository.py
```

检查范围包括 frontmatter、中文入口、插件清单、触发评测和上游同步基线。CI 还执行 Python 3.11 语法与 Shell 语法检查。

本次最小 DOCX、PPTX 产物通过新版 validator。XLSX 回算在当前 macOS LibreOffice 环境超时，所以仍标记为待排查，不能用“同步完成”替代真实验证。

## 为什么保留部分英文 reference

API 模型、beta header、SDK 方法和平台差异变化很快。把所有事实性 reference 翻译一遍，会形成第二套容易过期的真相。

因此 `claude-api` 采用中文任务路由 + 官方事实参考：中文入口负责识别意图和语言，具体 API 事实仍回到对应 SDK 文档和实时官方来源。

下一步是每周自动发现上游变化、完成中文本土化、跑验证并生成多平台技术文章草稿。自动化负责准备，公开发布仍经过预览确认。

项目地址：https://github.com/MarcelLeon/skills-zh
