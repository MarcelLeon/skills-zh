#!/usr/bin/env python3
"""
Skills 快速验证脚本 - 最小版本
"""

import sys
import os
import re
import yaml
from pathlib import Path

def validate_skill(skill_path):
    """Skill 的基本验证"""
    skill_path = Path(skill_path)

    # 检查 SKILL.md 是否存在
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "未找到 SKILL.md"

    # 读取并验证 frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "未找到 YAML frontmatter"

    # 提取 frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "无效的 frontmatter 格式"

    frontmatter_text = match.group(1)

    # 解析 YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter 必须是 YAML 字典"
    except yaml.YAMLError as e:
        return False, f"Frontmatter 中的 YAML 无效：{e}"

    # 定义允许的属性
    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata'}

    # 检查意外的属性（不包括 metadata 下的嵌套键）
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"SKILL.md frontmatter 中有意外的键：{', '.join(sorted(unexpected_keys))}。"
            f"允许的属性为：{', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # 检查必需字段
    if 'name' not in frontmatter:
        return False, "Frontmatter 中缺少 'name'"
    if 'description' not in frontmatter:
        return False, "Frontmatter 中缺少 'description'"

    # 提取 name 进行验证
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name 必须是字符串，但得到 {type(name).__name__}"
    name = name.strip()
    if name:
        # 检查命名约定（连字符大小写：小写字母和连字符）
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' 应为连字符大小写（仅限小写字母、数字和连字符）"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' 不能以连字符开头/结尾或包含连续的连字符"
        # 检查 name 长度（根据规范最多 64 个字符）
        if len(name) > 64:
            return False, f"Name 太长（{len(name)} 个字符）。最多 64 个字符。"

    # 提取并验证 description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description 必须是字符串，但得到 {type(description).__name__}"
    description = description.strip()
    if description:
        # 检查尖括号
        if '<' in description or '>' in description:
            return False, "Description 不能包含尖括号（< 或 >）"
        # 检查 description 长度（根据规范最多 1024 个字符）
        if len(description) > 1024:
            return False, f"Description 太长（{len(description)} 个字符）。最多 1024 个字符。"

    return True, "Skill 有效！"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法：python quick_validate.py <skill_directory>")
        sys.exit(1)
    
    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
