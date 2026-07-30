---
name: pptx
description: "只要 .pptx 或 .potx 参与任务，就必须使用本技能，无论它是输入、输出还是中间材料。中文触发包括：做汇报 PPT、路演稿、培训课件、读/改现有演示文稿、套公司模板、合并拆分页面、调整母版布局、讲稿备注或批注。用户只说“做几页汇报”“把方案整理成 slides”，只要需要真正交付或读取幻灯片也应触发；仅讨论演讲提纲且不操作 PPT 文件时不触发。"
license: Proprietary. LICENSE.txt has complete terms
---

# PPTX 创建、编辑与分析

`.pptx`/`.potx` 是包含 OOXML 的 ZIP 包。按任务选择：

| 任务 | 方法 |
| --- | --- |
| 新建演示稿 | 使用 `pptxgenjs` |
| 修改现有稿或模板 | 解包 → 调整结构 → 编辑 XML → 清理 → 压缩 |
| 读取内容 | `markitdown deck.pptx` |
| 观察全稿结构 | `python scripts/thumbnail.py deck.pptx deck-thumbs` |

脚本路径均相对于本 Skill 目录。

## 中文任务 few-shot

**输入：**“把这份 Data Agent 技术方案做成 12 页中文汇报，用公司模板，老板 10 分钟能讲完。”

**执行：**先提炼一条可讲述主线，再用缩略图选择不同模板布局；控制每页一个判断，保留公司母版，补讲稿备注，最后做内容、视觉和文件结构三轮检查。

**输入：**“roadmap.pptx 太密了，帮我重排但不要改事实。”

**执行：**先抽取文字和缩略图，建立事实清单；只重组层级和布局，不替换数据；输出前逐页渲染并核对原始事实。

## 可用脚本

| 脚本 | 用途 |
| --- | --- |
| `scripts/thumbnail.py deck.pptx prefix` | 生成带页码的全稿缩略图网格 |
| `scripts/add_slide.py unpacked/ slide2.xml --after slideN.xml` | 正确复制页面或 layout，并登记所有关系 |
| `scripts/clean.py unpacked/` | 在页面列表确定后清理孤立页面、媒体和关系 |
| `scripts/office/validate.py deck.pptx --original src.pptx` | 校验 schema、关系、content type、图表和页面 |
| `scripts/office/soffice.py --headless --convert-to pdf deck.pptx` | 在沙箱环境稳定调用 LibreOffice |

## 从零创建

`pptxgenjs` 通常已预装。先直接 `require("pptxgenjs")`，只有导入失败才安装。

高风险规则：

- 添加页面前先设置 `pres.layout`。`LAYOUT_16x9` 是 10 × 5.625 英寸，`LAYOUT_WIDE` 是 13.333 × 7.5 英寸。
- 颜色只写 6 位十六进制且不带 `#`；透明度使用对应属性，不写 8 位颜色。
- 不复用会被 pptxgenjs 原地修改的 options/shadow 对象。
- 阴影 `offset >= 0`；向上投影使用正 offset 配合 `angle: 270`。
- 文本对齐敏感时显式设置 `margin: 0`。
- 列表使用 `bullet: true`，不要手写 `•`。
- 每个输出文件使用独立的 `new pptxgen()` 实例。
- 讲稿备注使用 `slide.addNotes()`，不要放成页面文本框。
- PowerPoint 有原生图表时使用 `addChart()`；只有原生不支持的 Sankey、网络图等才转图片。
- stacked chart 的 `dataLabelPosition` 只能用 `ctr`、`inEnd`、`inBase`；错误配置会损坏文件。
- 组合图使用次坐标轴时，必须同时声明两组 `valAxes` 和 `catAxes`。
- 每次 `writeFile()` 后立即运行 `validate.py`，从生成脚本修问题，不手改打包后的 XML。

## 编辑现有演示稿

先生成缩略图并传入专属前缀，避免不同演示稿互相覆盖：

```bash
python scripts/thumbnail.py template.pptx template-thumbs
python -m markitdown template.pptx
```

结构编辑工作流：

```bash
python3 -c "import sys,zipfile; zipfile.ZipFile(sys.argv[1]).extractall('unpacked')" deck.pptx
find unpacked -type l -delete
python scripts/add_slide.py unpacked/ slide2.xml --after slide2.xml
# 在 ppt/presentation.xml 的 <p:sldIdLst> 调整顺序或删除页面
python scripts/clean.py unpacked/
# 编辑 ppt/slides/slideN.xml
(cd unpacked && rm -f ../output.pptx && zip -Xr ../output.pptx .)
python scripts/office/validate.py output.pptx --original deck.pptx
```

顺序必须是：先新增/删除/排序，再改页面内容。`add_slide.py` 会复制源页，若先编辑再复制，会意外克隆已改内容。

不要手工复制 `slideN.xml`。一个页面还涉及 presentation、rels、content type、notes 和媒体关系。

修改模板时：

- 模板槽位多于真实内容时，删除整个对象组，不只清空文字。
- 每个列表项使用独立 `<a:p>`。
- 替换文本时修改已有 run 的文本，避免 `text_frame.text = ...` 抹掉格式。
- 中文文本前后有空格时使用 `xml:space="preserve"`。
- 复用模板图标优先复制已有页面或 layout，不重新截图成低清位图。

## 中文汇报设计

先确定受众、会议时长和单一结论，再设计页面。

- 中文管理汇报优先“结论式标题”，标题直接表达本页判断，不写“项目背景”这类空标签。
- 一页只承担一个主要认知任务；长句拆为短段，正文避免字号过小。
- 公司模板、品牌色和既有版式优先，不以“设计感”为由破坏统一规范。
- 数据页优先原生图表和大数字；流程页用真正有方向的流程，不用无意义 01/02/03 装饰。
- 中文字体必须检查目标机器可用性；不要依赖只在本机安装的字体。
- 视觉母题只选一个，避免卡片、渐变、发光、玻璃效果同时堆叠。

### 避免常见 AI 幻灯片

- 每页都是“标题 + 三个圆角卡片”。
- 白底紫色渐变、随机装饰圆和无信息价值图标。
- 每页相同版式。
- 过度居中正文。
- 把 markdown、代码围栏或项目符号原样贴进页面。
- 为了填满版面编造数据或口号。

## 内容与视觉 QA

内容检查：

```bash
python -m markitdown output.pptx
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|placeholder"
python scripts/office/validate.py output.pptx
```

视觉检查：

```bash
rm -f slide-*.jpg
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
ls -1 "$PWD"/slide-*.jpg
```

逐页检查：

- 文本重叠、裁切和溢出。
- 中文字体替换导致的换行变化。
- 图表标签、单位、图例和数据范围。
- 页面边缘安全距离。
- 模板占位文本、虚构数据和无来源断言。
- 内容主线是否能在用户指定时长内讲完。

修复后必须重新生成 PDF 和全部页面图片，不能只看旧截图。

## 依赖

`pptxgenjs` · `markitdown[pptx]` · `Pillow` · `defusedxml` · `lxml` · LibreOffice · Poppler

