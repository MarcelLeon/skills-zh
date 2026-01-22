# Skills 中文版 | Skills Chinese Edition

[English](#english) | [中文](#中文)

---

<a name="中文"></a>

## 📖 关于本项目

这是 Claude Skills 样例库的**中文适配版本**，基于 [Anthropic 官方 Skills 仓库](https://github.com/anthropics/skills)改造而成。

本项目对所有 16 个官方 skills 进行了完整的中文化，包括：
- ✅ 翻译所有说明文档和指示内容
- ✅ 场景适配：将示例调整为更符合中文用户使用习惯
- ✅ 术语统一：建立完整的中英文术语对照表
- ✅ 保持功能完整性：所有脚本和代码保持可执行性

### 🔄 模型适配说明

本项目中的 skills 默认是为 **Claude 模型**编写的，文档中多处包含"Claude"字样。如果您想将这些 skills 适配到其他大语言模型，可以使用以下命令批量替换：

#### macOS/Linux 系统：

```bash
# 替换所有 skills 文件中的 "Claude" 为您的模型名称
# 注意：此命令会区分大小写，精确匹配 "Claude"

find ./skills -type f \( -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.html" \) \
  -exec sed -i '' 's/Claude/[您的大模型名称]/g' {} +

# 示例：替换为 "GPT"
find ./skills -type f \( -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.html" \) \
  -exec sed -i '' 's/Claude/GPT/g' {} +

# 示例：替换为 "Qwen"
find ./skills -type f \( -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.html" \) \
  -exec sed -i '' 's/Claude/Qwen/g' {} +
```

#### Windows 系统（Git Bash 或 WSL）：

```bash
# Windows 下使用 sed（无需 '' 参数）
find ./skills -type f \( -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.html" \) \
  -exec sed -i 's/Claude/[您的大模型名称]/g' {} +
```

#### 大小写变体处理：

如果需要同时替换不同大小写形式（如 Claude, claude, CLAUDE），使用以下命令：

```bash
# macOS/Linux - 替换所有大小写变体
find ./skills -type f \( -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.html" \) \
  -exec sed -i '' -E 's/Claude|claude|CLAUDE/[您的大模型名称]/g' {} +

# Windows (Git Bash/WSL)
find ./skills -type f \( -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.html" \) \
  -exec sed -i -E 's/Claude|claude|CLAUDE/[您的大模型名称]/g' {} +
```

**⚠️ 重要提示：**
1. 替换前建议先备份或使用 Git 版本控制
2. 替换后需要测试验证功能是否正常
3. 某些技术术语（如"Claude API"）可能需要手动调整
4. 建议先在单个文件上测试命令，确认效果后再批量执行

### 📂 项目结构

```
skills-zh/
├── README.md                    # 本文件（中英文双语）
├── skills/                      # 所有 skills（已中文化）
│   ├── skill-creator/          # Skill 创建工具
│   ├── docx/                   # Word 文档生成
│   ├── pdf/                    # PDF 文档生成
│   ├── pptx/                   # PowerPoint 演示文稿生成
│   ├── xlsx/                   # Excel 表格生成
│   ├── mcp-builder/            # MCP 服务器构建
│   ├── webapp-testing/         # Web 应用测试
│   ├── web-artifacts-builder/  # Web 工件构建
│   ├── internal-comms/         # 内部沟通
│   ├── brand-guidelines/       # 品牌指南
│   ├── canvas-design/          # 画布设计
│   ├── theme-factory/          # 主题工厂
│   ├── slack-gif-creator/      # Slack GIF 创建
│   ├── algorithmic-art/        # 算法艺术
│   ├── doc-coauthoring/        # 文档共同撰写
│   └── frontend-design/        # 前端设计
├── spec/                       # Agent Skills 规范
└── template/                   # Skill 模板
```

### 🎯 Skill 分类

#### 📄 文档类工具
- **docx** - 创建格式化的 Word 文档
- **pdf** - 生成专业的 PDF 文档
- **pptx** - 制作精美的 PowerPoint 演示文稿
- **xlsx** - 创建数据丰富的 Excel 表格
- **doc-coauthoring** - 结构化文档共同撰写工作流

#### 🛠️ 开发工具类
- **skill-creator** - 创建和验证新 skills 的工具
- **mcp-builder** - 构建 MCP（Model Context Protocol）服务器
- **webapp-testing** - Web 应用自动化测试
- **web-artifacts-builder** - Web 工件构建工具

#### 🎨 创意与设计类
- **algorithmic-art** - 使用 p5.js 创建算法艺术
- **canvas-design** - 画布设计工具
- **frontend-design** - 创建高质量前端界面
- **theme-factory** - 主题生成工厂

#### 💼 企业与沟通类
- **internal-comms** - 内部沟通消息生成
- **brand-guidelines** - 品牌指南应用
- **slack-gif-creator** - 为 Slack 创建动画 GIF

### 🚀 使用方法

#### 方法 1：在支持 Skills 的平台中使用

如果您使用的 AI 平台支持 Skills 功能，可以直接将 `skills/` 目录下的任何 skill 文件夹上传使用。

#### 方法 2：作为提示词参考

即使平台不支持 Skills，您也可以将 `SKILL.md` 文件中的内容作为高质量提示词模板参考。

#### 方法 3：使用 skill-creator 创建自定义 Skill

```bash
cd skills/skill-creator
python3 scripts/init_skill.py
# 按提示输入 skill 名称和描述
```

### 📚 相关资源

- **原项目仓库**: [anthropics/skills](https://github.com/anthropics/skills)
- **Agent Skills 规范**: [agentskills.io](http://agentskills.io)
- **术语对照表**: 请参考各 skill 中的注释说明

### ⚖️ 许可证

- 大部分 skills: Apache 2.0 开源许可证
- 文档类 skills (docx/pdf/pptx/xlsx): 源码可见但非开源，仅供参考
- 中文化改造内容: 遵循原项目许可证

### 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进中文化质量或添加新的中文 skills。

---

<a name="english"></a>

## 📖 About This Project

This is a **Chinese-adapted version** of the Claude Skills repository, based on the [official Anthropic Skills repository](https://github.com/anthropics/skills).

This project provides complete Chinese localization for all 16 official skills, including:
- ✅ Translation of all documentation and instructions
- ✅ Scenario adaptation: Examples adjusted for Chinese user habits
- ✅ Terminology standardization: Complete Chinese-English terminology mapping
- ✅ Maintained functionality: All scripts and code remain executable

### 🔄 Model Adaptation Guide

The skills in this project are written for **Claude** by default, with "Claude" mentioned throughout the documentation. If you want to adapt these skills for other large language models, use the following commands for batch replacement:

#### macOS/Linux:

```bash
# Replace "Claude" with your model name in all skills files
# Note: This command is case-sensitive and matches "Claude" exactly

find ./skills -type f \( -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.html" \) \
  -exec sed -i '' 's/Claude/[YourModelName]/g' {} +

# Example: Replace with "GPT"
find ./skills -type f \( -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.html" \) \
  -exec sed -i '' 's/Claude/GPT/g' {} +

# Example: Replace with "Qwen"
find ./skills -type f \( -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.html" \) \
  -exec sed -i '' 's/Claude/Qwen/g' {} +
```

#### Windows (Git Bash or WSL):

```bash
# Windows sed (no '' parameter needed)
find ./skills -type f \( -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.html" \) \
  -exec sed -i 's/Claude/[YourModelName]/g' {} +
```

#### Case Variant Handling:

To replace different case variants simultaneously (Claude, claude, CLAUDE):

```bash
# macOS/Linux - Replace all case variants
find ./skills -type f \( -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.html" \) \
  -exec sed -i '' -E 's/Claude|claude|CLAUDE/[YourModelName]/g' {} +

# Windows (Git Bash/WSL)
find ./skills -type f \( -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.html" \) \
  -exec sed -i -E 's/Claude|claude|CLAUDE/[YourModelName]/g' {} +
```

**⚠️ Important Notes:**
1. Backup or use Git version control before replacement
2. Test functionality after replacement
3. Some technical terms (e.g., "Claude API") may need manual adjustment
4. Test the command on a single file first before batch execution

### 📂 Project Structure

```
skills-zh/
├── README.md                    # This file (bilingual)
├── skills/                      # All skills (Chinese localized)
│   ├── skill-creator/          # Skill creation tool
│   ├── docx/                   # Word document generation
│   ├── pdf/                    # PDF document generation
│   ├── pptx/                   # PowerPoint presentation generation
│   ├── xlsx/                   # Excel spreadsheet generation
│   ├── mcp-builder/            # MCP server builder
│   ├── webapp-testing/         # Web application testing
│   ├── web-artifacts-builder/  # Web artifact builder
│   ├── internal-comms/         # Internal communications
│   ├── brand-guidelines/       # Brand guidelines
│   ├── canvas-design/          # Canvas design
│   ├── theme-factory/          # Theme factory
│   ├── slack-gif-creator/      # Slack GIF creator
│   ├── algorithmic-art/        # Algorithmic art
│   ├── doc-coauthoring/        # Document co-authoring
│   └── frontend-design/        # Frontend design
├── spec/                       # Agent Skills specification
└── template/                   # Skill template
```

### 🎯 Skill Categories

#### 📄 Document Tools
- **docx** - Create formatted Word documents
- **pdf** - Generate professional PDF documents
- **pptx** - Create beautiful PowerPoint presentations
- **xlsx** - Create data-rich Excel spreadsheets
- **doc-coauthoring** - Structured document co-authoring workflow

#### 🛠️ Development Tools
- **skill-creator** - Tool for creating and validating new skills
- **mcp-builder** - Build MCP (Model Context Protocol) servers
- **webapp-testing** - Web application automated testing
- **web-artifacts-builder** - Web artifact builder

#### 🎨 Creative & Design
- **algorithmic-art** - Create algorithmic art using p5.js
- **canvas-design** - Canvas design tool
- **frontend-design** - Create high-quality frontend interfaces
- **theme-factory** - Theme generation factory

#### 💼 Enterprise & Communication
- **internal-comms** - Internal communication message generation
- **brand-guidelines** - Brand guidelines application
- **slack-gif-creator** - Create animated GIFs for Slack

### 🚀 Usage

#### Method 1: Use in Skills-Enabled Platforms

If your AI platform supports Skills, you can upload any skill folder from `skills/` directory directly.

#### Method 2: As Prompt Reference

Even if your platform doesn't support Skills, you can use the content in `SKILL.md` files as high-quality prompt templates.

#### Method 3: Create Custom Skills with skill-creator

```bash
cd skills/skill-creator
python3 scripts/init_skill.py
# Follow prompts to enter skill name and description
```

### 📚 Resources

- **Original Repository**: [anthropics/skills](https://github.com/anthropics/skills)
- **Agent Skills Specification**: [agentskills.io](http://agentskills.io)
- **Terminology Reference**: See comments in individual skills

### ⚖️ License

- Most skills: Apache 2.0 open source license
- Document skills (docx/pdf/pptx/xlsx): Source-available but not open source, for reference only
- Chinese localization: Follows original project license

### 🤝 Contributing

Issues and Pull Requests are welcome to improve Chinese localization quality or add new Chinese skills.

---

## 🌟 Star History

If you find this project helpful, please consider giving it a star! ⭐

---

**项目状态 | Project Status**: ✅ 已完成中文化 | Chinese Localization Complete

**最后更新 | Last Update**: 2026-01-22
