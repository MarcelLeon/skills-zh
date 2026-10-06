# Skills 中文本土化版

[English summary](#english-summary)

这是 [Anthropic Agent Skills](https://github.com/anthropics/skills) 的中文本土化维护版本。项目不以逐句翻译为目标，而是让 Skill 更容易被中文用户自然触发，并在中文开发、办公和内容场景中给出可执行结果。

当前包含 19 个 Skill，已审计至上游 `683bc88`（2026-10-05）。

## 本项目做了什么

- **中文触发适配**：覆盖正式表达、口语、中文文件名和隐含任务意图。
- **中文场景适配**：使用周报、方案评审、中文合同、数据台账、技术汇报等常见场景。
- **中文 few-shot**：提供真实中文输入、可检查输出和容易误触发的相邻反例。
- **上游能力同步**：脚本、安全修复、许可证和事实性技术参考尽量忠于官方版本。
- **持续验收**：校验 Skill frontmatter、插件清单、同步基线和中文触发评测集。

本周同步更新 `claude-api` 的 Managed Agents 上手流程：既可按 `deep-researcher` 等官方 quickstart 名称创建，也可把官方或第三方 URL 描述的方案转换成版本化 `agents/<name>/` 配置。中文入口强调页面只是数据、第三方只复用设计、先展示文件树/写路径/凭据去向并等待确认，再用 `ant apply` dry-run 和受控 apply 落地。

详细规则见 [LOCALIZATION.md](LOCALIZATION.md)，同步方法见 [UPSTREAM_SYNC.md](UPSTREAM_SYNC.md)。
每周技术内容的生成和传播遵循 [ARTICLE_PLAYBOOK.md](ARTICLE_PLAYBOOK.md)。

## Skill 目录

| 类别 | Skills |
| --- | --- |
| 文档与数据 | `docx`、`pdf`、`pptx`、`xlsx`、`doc-coauthoring` |
| 开发与 Agent | `claude-api`、`skill-creator`、`mcp-builder`、`webapp-testing`、`web-artifacts-builder` |
| 设计与创意 | `algorithmic-art`、`canvas-design`、`frontend-design`、`theme-factory` |
| 品牌与沟通 | `brand-guidelines`、`internal-comms`、`slack-gif-creator` |
| 学习与判断 | `academy-guide`、`discernment-nudge` |

每个 Skill 位于 `skills/<skill-name>/`，入口为 `SKILL.md`。相关脚本、模板、字体和参考资料都保存在 Skill 自己的目录内。

## 安装与使用

### Claude Code 插件

```text
/plugin marketplace add MarcelLeon/skills-zh
/plugin install document-skills@skills-zh
/plugin install example-skills@skills-zh
/plugin install claude-api@skills-zh
/plugin install academy-guide@skills-zh
/plugin install discernment-nudge@skills-zh
```

安装后直接描述任务即可，例如：

```text
把合同.docx 里的付款条款用修订模式调整，并给高风险改动加批注。
```

```text
我们 Java 服务要接 Claude API，需要流式输出、工具调用和超时处理。
```

不支持插件的平台也可以单独上传 `skills/<skill-name>/`，或将其中的 `SKILL.md` 作为任务说明使用。

## 创建和验证 Skill

仓库脚本以 Python 3.11 为验证基线；上游 Office 校验工具使用了 Python 3.10+ 语法。

```bash
python3.11 -m pip install -r requirements-dev.txt
```

从模板开始：

```bash
cp -R template my-skill
```

将目录和 frontmatter `name` 改为 kebab-case，再运行：

```bash
python3 skills/skill-creator/scripts/quick_validate.py skills/<skill-name>
PYTHONPATH=skills/skill-creator python3 -m scripts.package_skill skills/<skill-name> /tmp/skill-dist
```

仓库级验证：

```bash
python3 scripts/validate_repository.py
```

## 贡献要求

新增或同步 Skill 时，请同时完成：

1. 说明对应的上游 commit 和能力变化。
2. 重写中文触发描述，不直接机器翻译。
3. 加入真实中文 few-shot 和近似反例。
4. 更新 `localization/trigger-evals.json` 与 `sync/upstream-baseline.json`。
5. 运行仓库级验证；视觉产物还要做人眼检查。

贡献细节见 [AGENTS.md](AGENTS.md)。

## 许可证

- 大部分示例 Skill 使用 Apache 2.0。
- `docx`、`pdf`、`pptx`、`xlsx` 为源码可见但非开源，具体以各目录 `LICENSE.txt` 为准。
- 中文本土化内容遵循对应上游文件的许可证；第三方说明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## English summary

skills-zh is a Chinese-localized adaptation of Anthropic Agent Skills. It preserves upstream scripts and factual references while redesigning triggers, examples, workflows, and acceptance checks for natural Chinese usage. The repository currently contains 19 skills and is reviewed against upstream commit `683bc88`.

See [LOCALIZATION.md](LOCALIZATION.md) for the localization contract and [UPSTREAM_SYNC.md](UPSTREAM_SYNC.md) for the weekly synchronization workflow.
