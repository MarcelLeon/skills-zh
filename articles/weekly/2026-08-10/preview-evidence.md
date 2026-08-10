# 2026-08-10 多平台发布确认单

## 门禁结论

截至 2026-08-10 14:50（Asia/Shanghai），六个平台 payload 已通过本地 validator，平台可见页面已用于核对登录态和账号。没有把标题、正文、图片或标签传入平台，没有创建或更新远程草稿，也没有点击最终发布。

用户确认本文件所列账号、标题、正文文件、标签/分类/节点、图片和公开模式后，才进入平台编辑器填充与渲染预览；渲染证据复核通过后，再单独请求最终发布确认。

## 待确认 payload

| 平台 | 账号 | 最终标题 | 分类 / 标签 / 节点 | 图片 | 目标模式 | 当前状态 |
| --- | --- | --- | --- | --- | --- | --- |
| 博客园 | 已登录，精确账号仅记录在本地确认单 | skills-zh 2026.08.10 发布说明：Managed Agents 生产治理能力更新 | 分类 `AI`；`Claude API`、`Managed Agents`、`Agent Skills`、`多 Agent`；勾选 AI 生成声明 | 无 | 公开 | 编辑器可用，待确认后填充 |
| 掘金 | 已登录，精确账号仅记录在本地确认单 | skills-zh 发布说明：Managed Agents 生产治理能力更新 | 分类 `人工智能`；`Claude`、`Agent`、`多Agent`、`开发工具` | 待使用第 1 张卡片作为封面并检查裁切 | 公开 | 编辑器可用，待确认后填充；编辑器会自动保存草稿 |
| Bilibili | 已登录，精确账号仅记录在本地确认单 | skills-zh 2026.08.10 发布说明：Managed Agents 生产治理更新 | `Claude`、`Agent`、`多Agent`、`开发工具`；勾选 AI 辅助创作声明 | 第 1 张卡片，待检查封面裁切 | 所有人可见 | 专栏编辑器可用，待确认后填充 |
| 小红书 | 当前 Chrome 未登录 | skills-zh周更：Agent治理升级 | `AIAgent`、`Claude`、`开发者工具`、`多Agent`；按平台要求声明 AI 图片 | `card-01.png` 至 `card-07.png` | 公开图文 | 7 张图片与正文就绪；需用户自行完成短信登录 |
| LinkedIn | 已登录，精确账号仅记录在本地确认单 | skills-zh 2026.08.10 release: production governance for Managed Agents | `AI`、`Agents`、`Claude`、`DeveloperTools` | 无 | 公开动态 | 账号已登录，待确认后填充 |
| V2EX | 已登录但未激活，精确账号仅记录在本地确认单 | skills-zh 本周发布：大家会把 Agent 治理放在哪一层验收？ | 节点 `programmer` | 无 | 公开主题 | 账号要求邀请码激活，当前不可发布 |

正文以同目录对应文件为唯一版本：`cnblogs.md`、`juejin.md`、`bilibili.md`、`xiaohongshu.md`、`linkedin.md`、`v2ex.md`。项目链接统一为 `https://github.com/MarcelLeon/skills-zh`。

## 小红书图片顺序

1. `assets/xhs/card-01.png`：封面，Managed Agents 生产治理更新。
2. `assets/xhs/card-02.png`：上游范围与变化规模。
3. `assets/xhs/card-03.png`：Session / Deployment 预算。
4. `assets/xhs/card-04.png`：Inference Geo 与仓库 Skills 信任边界。
5. `assets/xhs/card-05.png`：Multiagent 与 Advisor 分工。
6. `assets/xhs/card-06.png`：中文本土化和验证数据。
7. `assets/xhs/card-07.png`：交付状态、Draft PR 与真实 API 验证限制。

## 仍需用户动作

- 确认上述五个可用账号的最终 payload 与公开模式；V2EX 暂不纳入本轮发布。
- 如需发布小红书，先在 Chrome 中自行完成短信登录；自动化不会读取或代填验证码。
- 平台填充后还会返回实际渲染截图与发布设置，最终发布按钮需要再次明确确认。
