---
name: mcp-builder
description: 创建、改造、审查或迁移高质量 MCP（Model Context Protocol）服务器，让 LLM 通过设计清晰的工具与外部服务交互。当用户说“把这个 API 接成 MCP”“给 Agent 加工具”“做一个 MCP Server”，或要使用 Python/FastMCP、TypeScript MCP SDK、`@modelcontextprotocol/server` v2、从 `@modelcontextprotocol/sdk` v1 升级时使用；也适用于工具 schema、分页、鉴权、stdio/Streamable HTTP、自检脚本和评测设计。
license: Complete terms in LICENSE.txt
---

# MCP 服务器开发指南

## 概述

创建 MCP（Model Context Protocol）服务器，使 LLM 能够通过精心设计的工具与外部服务交互。MCP 服务器的质量通过它如何有效地使 LLM 完成现实世界任务来衡量。

---

# 流程

## 🚀 高级工作流程

创建高质量 MCP 服务器涉及四个主要阶段：

### 阶段 1：深入研究和规划

#### 1.1 理解现代 MCP 设计

**API 覆盖率 vs. 工作流工具：**
平衡全面的 API 端点覆盖与专门的工作流工具。工作流工具对于特定任务可能更方便，而全面的覆盖率为代理提供了组合操作的灵活性。性能因客户端而异——一些客户端受益于组合基本工具的代码执行，而其他客户端使用更高级别的工作流效果更好。如果不确定，优先考虑全面的 API 覆盖率。

**工具命名和可发现性：**
清晰、描述性的工具名称帮助代理快速找到正确的工具。使用一致的前缀（例如，`github_create_issue`、`github_list_repos`）和面向操作的命名。

**上下文管理：**
代理受益于简洁的工具描述以及过滤/分页结果的能力。设计返回集中、相关数据的工具。一些客户端支持代码执行，这可以帮助代理高效地过滤和处理数据。

**可操作的错误消息：**
错误消息应该通过具体建议和后续步骤引导代理找到解决方案。

#### 1.2 学习 MCP 协议文档

**浏览 MCP 规范：**

从站点地图开始查找相关页面：`https://modelcontextprotocol.io/sitemap.xml`

然后使用 `.md` 后缀获取特定页面的 markdown 格式（例如，`https://modelcontextprotocol.io/specification/draft.md`）。

需要查看的关键页面：
- 规范概述和架构
- 传输机制（可流式 HTTP、stdio）
- 工具、资源和提示定义

#### 1.3 学习框架文档

**推荐技术栈：**
- **语言**：TypeScript（高质量 SDK 支持，在许多执行环境中具有良好兼容性，例如 MCPB。此外，AI 模型擅长生成 TypeScript 代码，受益于其广泛使用、静态类型和良好的 lint 工具）
- **传输**：远程服务器使用可流式 HTTP，使用无状态 JSON（相对于有状态会话和流式响应，更易于扩展和维护）。本地服务器使用 stdio。

**加载框架文档：**

- **MCP 最佳实践**：[📋 查看最佳实践](./reference/mcp_best_practices.md) - 核心指南

**对于 TypeScript（推荐）：**

TypeScript SDK 有两个主要版本，写代码前先根据项目依赖选择：
- **v2**（`@modelcontextprotocol/server`）：当前稳定版，新建服务器默认使用。
- **v1**（`@modelcontextprotocol/sdk`）：只接收 bug 和安全修复。仅当现有项目的 `package.json` 已依赖它时继续使用，或按用户要求运行 `npx @modelcontextprotocol/codemod@latest v1-to-v2 .` 迁移。

如果项目已经使用 v1，用一两句话告知用户：v2（`@modelcontextprotocol/server`）是当前稳定版，v1 只接收 bug 与安全修复，官方 codemod 可以迁移。除非用户明确要求升级，否则随后继续按 v1 实现。

不要在同一项目混用两个版本：从 `@modelcontextprotocol/sdk/...` 导入的 v1 示例不能直接用于 v2。

- **TypeScript SDK（v2）**：使用 WebFetch 加载 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`；完整文档索引为 `https://ts.sdk.modelcontextprotocol.io/v2/llms.txt`
- [⚡ TypeScript 指南（v2）](./reference/node_mcp_server_v2.md) - v2 模式、完整示例与自检
- 仅现有 v1 项目：读取 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/v1.x/README.md` 和 [TypeScript 指南（v1）](./reference/node_mcp_server.md)

**对于 Python：**
- **Python SDK**：使用 WebFetch 加载 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python 指南](./reference/python_mcp_server.md) - Python 模式和示例

#### 1.4 规划您的实现

**理解 API：**
查看服务的 API 文档以识别关键端点、身份验证要求和数据模型。根据需要使用网络搜索和 WebFetch。

**工具选择：**
优先考虑全面的 API 覆盖率。列出要实现的端点，从最常见的操作开始。

#### 1.5 中文任务示例

**示例 1：新建 TypeScript MCP 服务**

输入：“把工单 API 封装成 TypeScript MCP Server，本地给 IDE 用 stdio，远程部署走 Streamable HTTP 和 Bearer 鉴权；请给可运行代码和 smoke test。”

执行要点：
- 项目没有 v1 依赖，选择 `@modelcontextprotocol/server` v2、Zod 4 和 `createServer()` 工厂。
- 工具 schema 带约束与描述，列表接口支持分页，远程路由保留 Host/Origin 校验并验证访问令牌。
- 同一份实现支持 stdio 与 HTTP；运行 `npm run build` 和 v2 指南中的自检脚本。

验收：依赖和 import 不混入 v1；stdio 不向 stdout 打日志；自检能列出工具、调用只读工具并拒绝非法参数。

**示例 2：现有 v1 项目继续维护或迁移**

输入：“这个仓库还在用 `@modelcontextprotocol/sdk`，先帮我加一个查订单工具；如果迁 v2 风险不大，也给出升级步骤，但不要擅自改完整个项目。”

执行要点：
- 先读 `package.json`，确认项目是 v1；用一两句话说明 v2 现状和 `v1-to-v2` codemod。
- 用户没有明确要求迁移时，继续读取 v1 指南实现新工具，不复制 v2 的 import、Zod 4 或 handler context 写法。
- 若用户选择迁移，再运行 codemod，检查 `@mcp-codemod-error`、Zod 版本、TypeScript 编译和原有测试。

验收：新增功能与现有 v1 项目兼容；迁移方案与功能改动分开；没有在一次提交里混合两套 SDK。

---

### 阶段 2：实现

#### 2.1 设置项目结构

有关项目设置，请参见特定语言的指南：
- [⚡ TypeScript 指南（v2）](./reference/node_mcp_server_v2.md) - 项目结构、package.json、tsconfig.json（现有 v1 项目使用 [v1 指南](./reference/node_mcp_server.md)）
- [🐍 Python 指南](./reference/python_mcp_server.md) - 模块组织、依赖项

#### 2.2 实现核心基础设施

创建共享实用程序：
- 带身份验证的 API 客户端
- 错误处理帮助程序
- 响应格式化（JSON/Markdown）
- 分页支持

#### 2.3 实现工具

对于每个工具：

**输入架构：**
- 使用 Zod (TypeScript) 或 Pydantic (Python)
- 包含约束和清晰的描述
- 在字段描述中添加示例

**输出架构：**
- 尽可能为结构化数据定义 `outputSchema`
- 在工具响应中使用 `structuredContent`（TypeScript SDK 功能）
- 帮助客户端理解和处理工具输出

**工具描述：**
- 功能的简洁总结
- 参数描述
- 返回类型架构

**实现：**
- I/O 操作使用 Async/await
- 带有可操作消息的正确错误处理
- 在适用的地方支持分页
- 使用现代 SDK 时返回文本内容和结构化数据

**注释：**
- `readOnlyHint`: true/false
- `destructiveHint`: true/false
- `idempotentHint`: true/false
- `openWorldHint`: true/false

---

### 阶段 3：审查和测试

#### 3.1 代码质量

审查以下内容：
- 无重复代码（DRY 原则）
- 一致的错误处理
- 完整的类型覆盖
- 清晰的工具描述

#### 3.2 构建和测试

**TypeScript：**
- 运行 `npm run build` 验证编译
- v2 项目：使用 [v2 指南](./reference/node_mcp_server_v2.md#verify-your-server) 的自检脚本验证已构建服务器
- 使用 MCP Inspector 测试：`npx @modelcontextprotocol/inspector`

**Python：**
- 验证语法：`python -m py_compile your_server.py`
- 使用 MCP Inspector 测试

有关详细的测试方法和质量检查清单，请参见特定语言的指南。

---

### 阶段 4：创建评估

实现 MCP 服务器后，创建全面的评估来测试其有效性。

**加载 [✅ 评估指南](./reference/evaluation.md) 以获取完整的评估指南。**

#### 4.1 理解评估目的

使用评估来测试 LLM 是否可以有效地使用您的 MCP 服务器回答现实的、复杂的问题。

#### 4.2 创建 10 个评估问题

要创建有效的评估，请遵循评估指南中概述的流程：

1. **工具检查**：列出可用工具并了解其功能
2. **内容探索**：使用只读操作探索可用数据
3. **问题生成**：创建 10 个复杂、现实的问题
4. **答案验证**：自己解决每个问题以验证答案

#### 4.3 评估要求

确保每个问题是：
- **独立的**：不依赖于其他问题
- **只读的**：仅需要非破坏性操作
- **复杂的**：需要多次工具调用和深入探索
- **现实的**：基于人类关心的真实用例
- **可验证的**：可以通过字符串比较验证的单一、清晰答案
- **稳定的**：答案不会随时间改变

#### 4.4 输出格式

创建具有此结构的 XML 文件：

```xml
<evaluation>
  <qa_pair>
    <question>查找关于使用动物代号的 AI 模型发布的讨论。一个模型需要特定的安全名称，格式为 ASL-X。为以斑点野猫命名的模型确定的数字 X 是多少？</question>
    <answer>3</answer>
  </qa_pair>
<!-- 更多 qa_pairs... -->
</evaluation>
```

---

# 参考文件

## 📚 文档库

在开发过程中根据需要加载这些资源：

### 核心 MCP 文档（首先加载）
- **MCP 协议**：从 `https://modelcontextprotocol.io/sitemap.xml` 的站点地图开始，然后使用 `.md` 后缀获取特定页面
- [📋 MCP 最佳实践](./reference/mcp_best_practices.md) - 通用 MCP 指南，包括：
  - 服务器和工具命名约定
  - 响应格式指南（JSON vs Markdown）
  - 分页最佳实践
  - 传输选择（可流式 HTTP vs stdio）
  - 安全和错误处理标准

### SDK 文档（在阶段 1/2 期间加载）
- **Python SDK**：从 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` 获取
- **TypeScript SDK（v2）**：从 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md` 获取；完整文档索引为 `https://ts.sdk.modelcontextprotocol.io/v2/llms.txt`
- **TypeScript SDK（v1，仅现有 v1 项目）**：从 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/v1.x/README.md` 获取

### 特定语言的实现指南（在阶段 2 期间加载）
- [🐍 Python 实现指南](./reference/python_mcp_server.md) - 完整的 Python/FastMCP 指南，包括：
  - 服务器初始化模式
  - Pydantic 模型示例
  - 使用 `@mcp.tool` 的工具注册
  - 完整的工作示例
  - 质量检查清单

- [⚡ TypeScript 实现指南（SDK v2）](./reference/node_mcp_server_v2.md) - 面向 `@modelcontextprotocol/server` 的完整指南，包括：
  - 项目设置与服务器工厂
  - Zod 4 schema、输出格式、分页和错误处理
  - 同时服务 stdio 与 Streamable HTTP 的完整示例，以及 Bearer 鉴权
  - 资源、提示词和通知
  - 验证已构建服务器的自检脚本
  - 高级特性的 SDK 示例链接
  - v1 → v2 对照、迁移步骤和质量检查清单

- [⚡ TypeScript 实现指南（SDK v1）](./reference/node_mcp_server.md) - 现有 `@modelcontextprotocol/sdk` 项目的等价指南

### 评估指南（在阶段 4 期间加载）
- [✅ 评估指南](./reference/evaluation.md) - 完整的评估创建指南，包括：
  - 问题创建指南
  - 答案验证策略
  - XML 格式规范
  - 示例问题和答案
  - 使用提供的脚本运行评估
