#!/usr/bin/env python3
"""
Skill 初始化工具 - 从模板创建新的 skill

用法：
    init_skill.py <skill-name> --path <path>

示例：
    init_skill.py my-new-skill --path skills/public
    init_skill.py my-api-helper --path skills/private
    init_skill.py custom-skill --path /custom/location
"""

import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: 完整且详细地说明 skill 的功能和使用时机。包括何时使用此 skill - 具体场景、文件类型或触发任务。]
---

# {skill_title}

## 概述

[TODO: 用 1-2 句话说明此 skill 的功能]

## 组织此 Skill 的结构

[TODO: 选择最适合此 skill 目的的结构。常见模式：

**1. 基于工作流程**（最适合顺序流程）
- 当有清晰的逐步流程时效果很好
- 示例：DOCX skill 使用"工作流程决策树" → "读取" → "创建" → "编辑"
- 结构：## 概述 → ## 工作流程决策树 → ## 步骤 1 → ## 步骤 2...

**2. 基于任务**（最适合工具集合）
- 当 skill 提供不同的操作/功能时效果很好
- 示例：PDF skill 使用"快速入门" → "合并 PDF" → "拆分 PDF" → "提取文本"
- 结构：## 概述 → ## 快速入门 → ## 任务类别 1 → ## 任务类别 2...

**3. 参考/指南**（最适合标准或规范）
- 适用于品牌指南、编码标准或要求
- 示例：品牌样式使用"品牌指南" → "颜色" → "排版" → "功能"
- 结构：## 概述 → ## 指南 → ## 规范 → ## 用法...

**4. 基于功能**（最适合集成系统）
- 当 skill 提供多个相互关联的功能时效果很好
- 示例：产品管理使用"核心功能" → 编号的功能列表
- 结构：## 概述 → ## 核心功能 → ### 1. 功能 → ### 2. 功能...

模式可以根据需要混合搭配。大多数 skills 组合多种模式（例如，从基于任务开始，为复杂操作添加工作流程）。

完成后删除整个"组织此 Skill 的结构"部分 - 这只是指导。]

## [TODO: 根据选择的结构替换为第一个主要部分]

[TODO: 在此处添加内容。参见现有 skills 中的示例：
- 技术 skills 的代码示例
- 复杂工作流程的决策树
- 具有实际用户请求的具体示例
- 根据需要引用 scripts/templates/references]

## 资源

此 skill 包含示例资源目录，演示如何组织不同类型的捆绑资源：

### scripts/
可直接运行以执行特定操作的可执行代码（Python/Bash 等）。

**来自其他 skills 的示例：**
- PDF skill：`fill_fillable_fields.py`、`extract_form_field_info.py` - PDF 操作实用工具
- DOCX skill：`document.py`、`utilities.py` - 文档处理的 Python 模块

**适用于：** Python 脚本、Shell 脚本或任何执行自动化、数据处理或特定操作的可执行代码。

**注意：** 脚本可以在不加载到上下文的情况下执行，但 Claude 仍可以读取它们以进行修补或环境调整。

### references/
旨在加载到上下文中以指导 Claude 的流程和思考的参考文档和参考资料。

**来自其他 skills 的示例：**
- 产品管理：`communication.md`、`context_building.md` - 详细的工作流程指南
- BigQuery：API 参考文档和查询示例
- 财务：架构文档、公司政策

**适用于：** 深入的文档、API 参考、数据库架构、综合指南，或 Claude 在工作时应参考的任何详细信息。

### assets/
不打算加载到上下文中，而是在 Claude 生成的输出中使用的文件。

**来自其他 skills 的示例：**
- 品牌样式：PowerPoint 模板文件（.pptx）、徽标文件
- 前端构建器：HTML/React 样板项目目录
- 排版：字体文件（.ttf、.woff2）

**适用于：** 模板、样板代码、文档模板、图像、图标、字体，或任何要在最终输出中复制或使用的文件。

---

**可以删除任何不需要的目录。** 并非每个 skill 都需要所有三种类型的资源。
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
{skill_name} 的示例辅助脚本

这是一个可以直接执行的占位符脚本。
根据实际需求替换或删除。

来自其他 skills 的实际脚本示例：
- pdf/scripts/fill_fillable_fields.py - 填充 PDF 表单字段
- pdf/scripts/convert_pdf_to_images.py - 将 PDF 页面转换为图像
"""

def main():
    print("这是 {skill_name} 的示例脚本")
    # TODO: 在此处添加实际的脚本逻辑
    # 这可以是数据处理、文件转换、API 调用等。

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# {skill_title} 的参考文档

这是详细参考文档的占位符。
根据实际参考内容替换或删除。

来自其他 skills 的实际参考文档示例：
- product-management/references/communication.md - 状态更新的综合指南
- product-management/references/context_building.md - 收集上下文的深入探讨
- bigquery/references/ - API 参考和查询示例

## 何时参考文档有用

参考文档适用于：
- 全面的 API 文档
- 详细的工作流程指南
- 复杂的多步骤流程
- 对于主 SKILL.md 来说太长的信息
- 仅在特定用例中需要的内容

## 结构建议

### API 参考示例
- 概述
- 认证
- 带示例的端点
- 错误代码
- 速率限制

### 工作流程指南示例
- 先决条件
- 逐步说明
- 常见模式
- 故障排除
- 最佳实践
"""

EXAMPLE_ASSET = """# 示例资源文件

此占位符表示资源文件的存储位置。
根据实际资源文件（模板、图像、字体等）替换或删除。

资源文件不打算加载到上下文中，而是在 Claude 生成的输出中使用。

来自其他 skills 的示例资源文件：
- 品牌指南：logo.png、slides_template.pptx
- 前端构建器：包含 HTML/React 样板的 hello-world/ 目录
- 排版：custom-font.ttf、font-family.woff2
- 数据：sample_data.csv、test_dataset.json

## 常见资源类型

- 模板：.pptx、.docx、样板目录
- 图像：.png、.jpg、.svg、.gif
- 字体：.ttf、.otf、.woff、.woff2
- 样板代码：项目目录、入门文件
- 图标：.ico、.svg
- 数据文件：.csv、.json、.xml、.yaml

注意：这是一个文本占位符。实际资源可以是任何文件类型。
"""


def title_case_skill_name(skill_name):
    """将连字符分隔的 skill 名称转换为标题大小写以供显示。"""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path):
    """
    使用模板 SKILL.md 初始化新的 skill 目录。

    参数：
        skill_name: skill 的名称
        path: 应创建 skill 目录的路径

    返回：
        创建的 skill 目录的路径，如果出错则返回 None
    """
    # 确定 skill 目录路径
    skill_dir = Path(path).resolve() / skill_name

    # 检查目录是否已存在
    if skill_dir.exists():
        print(f"❌ 错误：Skill 目录已存在：{skill_dir}")
        return None

    # 创建 skill 目录
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ 已创建 skill 目录：{skill_dir}")
    except Exception as e:
        print(f"❌ 创建目录时出错：{e}")
        return None

    # 从模板创建 SKILL.md
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content)
        print("✅ 已创建 SKILL.md")
    except Exception as e:
        print(f"❌ 创建 SKILL.md 时出错：{e}")
        return None

    # 创建带示例文件的资源目录
    try:
        # 创建带示例脚本的 scripts/ 目录
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example_script.chmod(0o755)
        print("✅ 已创建 scripts/example.py")

        # 创建带示例参考文档的 references/ 目录
        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / 'api_reference.md'
        example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("✅ 已创建 references/api_reference.md")

        # 创建带示例资源占位符的 assets/ 目录
        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        example_asset = assets_dir / 'example_asset.txt'
        example_asset.write_text(EXAMPLE_ASSET)
        print("✅ 已创建 assets/example_asset.txt")
    except Exception as e:
        print(f"❌ 创建资源目录时出错：{e}")
        return None

    # 打印后续步骤
    print(f"\n✅ Skill '{skill_name}' 已成功初始化，位于 {skill_dir}")
    print("\n后续步骤：")
    print("1. 编辑 SKILL.md 以完成 TODO 项并更新描述")
    print("2. 自定义或删除 scripts/、references/ 和 assets/ 中的示例文件")
    print("3. 准备好后运行验证器以检查 skill 结构")

    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("用法：init_skill.py <skill-name> --path <path>")
        print("\nSkill 名称要求：")
        print("  - 连字符大小写标识符（例如，'data-analyzer'）")
        print("  - 仅限小写字母、数字和连字符")
        print("  - 最多 40 个字符")
        print("  - 必须与目录名称完全匹配")
        print("\n示例：")
        print("  init_skill.py my-new-skill --path skills/public")
        print("  init_skill.py my-api-helper --path skills/private")
        print("  init_skill.py custom-skill --path /custom/location")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]

    print(f"🚀 正在初始化 skill：{skill_name}")
    print(f"   位置：{path}")
    print()

    result = init_skill(skill_name, path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
