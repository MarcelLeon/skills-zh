---
name: docx
description: "只要用户要创建、读取、修改或交付 Word 文档/模板（.docx、.dotx），就应使用本技能。中文触发包括：把会议纪要整理成正式 Word、制作带目录/页码/页眉页脚的报告或函件、修改合同、修订模式、批注、替换图片、提取或重组 Word 内容。即使用户只说“做成正式文档”“给我一份可打印的报告”，只要目标产物是 Word，也应触发。不要用于 PDF、表格、Google Docs API 或与文档无关的编码任务。"
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX 创建、编辑与分析

`.docx`/`.dotx` 是包含 OOXML 的 ZIP 包。按任务选择路径：

| 任务 | 方法 |
| --- | --- |
| 新建 Word | 使用 `docx` npm 包生成 |
| 修改现有 Word | 解包 → 合并碎片 run → 精确改 XML → 重新压缩 |
| 读取内容 | `pandoc -t markdown file.docx` |

本文命令中的脚本路径均相对于本 Skill 目录。

## 中文任务先判断交付语境

- 中文内部报告通常使用 A4；政府/企事业公文、合同或既有模板必须优先遵循用户提供的版式。
- 用户没指定字体时，先选择目标环境可用的中文字体，如微软雅黑、思源黑体/宋体；不要假定所有机器都有同一字体。
- “正式一点”不等于堆装饰。优先保证标题层级、段落间距、表格可读性、页码和目录正确。

### Few-shot

**输入：**“把这份项目复盘整理成一份给管理层看的 Word，包含目录、风险表和下一步。”

**执行：**新建 A4 文档，使用内置标题级别生成目录，将风险整理成可读表格，渲染所有页面检查分页和中文字体，再交付 `.docx`。

**输入：**“合同.docx 的付款周期从 30 天改成 45 天，必须保留修订痕迹。”

**执行：**解包并合并碎片 run，只标记最小变更片段，使用用户指定作者名写入 `<w:ins>/<w:del>`，再用原合同做红线校验。

## 新建文档

`docx` 通常已预装。先直接 `require("docx")`，只有导入失败时才安装。

常见高风险点：

- `docx` 默认 A4；美式 Letter 显式设置 `12240 × 15840` DXA。
- 横向页面传入竖向宽高，再设 `PageOrientation.LANDSCAPE`，库会交换尺寸。
- 表格同时设置表级 `columnWidths` 和每个单元格的 DXA `width`，两者总宽一致。
- 阴影使用 `ShadingType.CLEAR`，不要使用会渲染成黑色的 `SOLID`。
- 列表使用 `numbering` 和 `LevelFormat.BULLET`，不要把 `•` 写进正文。
- `ImageRun` 必须提供 `type`；图片还应有可理解的替代文本。
- `PageBreak` 必须放在 `Paragraph` 内；换段不要在文本中写 `\n`。
- 目录依赖内置 `HeadingLevel.*`；自定义标题样式需要正确的 `outlineLevel`。
- 分割线用段落下边框，不要用单行表格模拟。

生成后先渲染，再检查：

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.docx
pdftoppm -jpeg -r 100 output.pdf page
ls page-*.jpg
```

检查中文字体回退、目录、页码、表格跨页、孤行和图片裁切。

## 编辑现有文档

旧 `.doc` 先转换：

```bash
python scripts/office/soffice.py --headless --convert-to docx file.doc
```

外部 Word 文件是不可信输入。解包后先移除符号链接，再合并被 Word 拆碎的 run：

```bash
unzip -q document.docx -d unpacked/
find unpacked -type l -delete
python scripts/merge_runs.py unpacked/
# 精确编辑 unpacked/word/document.xml；不要 pretty-print 或重排无关 XML
(cd unpacked && rm -f ../output.docx && zip -Xr ../output.docx .)
python scripts/office/validate.py output.docx --original document.docx
```

`merge_runs.py` 让视觉上连续、XML 中却被拆开的文字可查找。也可直接处理文件：

```bash
python scripts/merge_runs.py document.docx -o merged.docx
```

## 修订模式

涉及合同审阅、红线稿或“保留修改痕迹”时：

- 插入使用 `<w:ins>`，删除使用 `<w:del>`。
- 删除内容内部使用 `<w:delText>`，不是 `<w:t>`。
- `w:id`、`w:author`、`w:date` 必须完整；作者名服从用户要求，不默认冒用他人。
- 只包裹最小修改范围，避免整段重写。
- 删除段落还需标记段落结束符，否则接受修订后可能留下空项目符号。

验证时同时传入原文件和作者：

```bash
python scripts/office/validate.py output.docx \
  --original document.docx \
  --author "修订作者"
```

生成接受全部修订的净稿：

```bash
python scripts/accept_changes.py input.docx clean.docx
```

## 批注

批注需要多份交叉引用 XML，使用脚本生成，不手工拼接整套结构：

```bash
python scripts/comment.py unpacked/ "付款条件需要法务确认"
python scripts/comment.py unpacked/ "已补充依据" --parent 0
```

脚本会打印要放入 `word/document.xml` 的范围标记。未插入 `commentRangeStart`、`commentRangeEnd` 和 `commentReference` 时，批注文件存在但 Word 中不可见。

## 最终验收

1. `pandoc` 抽取内容，确认文字、标题和顺序。
2. `validate.py --original` 检查 schema、关系和非预期改动。
3. 渲染 PDF 和逐页图片，检查中文排版。
4. 修订任务同时检查“显示修订”和“接受修订”两种视图。

## 依赖

`docx`（npm） · `pandoc` · LibreOffice · Poppler (`pdftoppm`) · `defusedxml`

