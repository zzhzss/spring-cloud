---
name: test-skill
description: 测试技能：用于验证 .claude/skills 目录是否被正确识别。当用户要求测试技能、检查技能加载或演示技能结构时使用。
---

# 测试技能（test-skill）

这是一个用于验证 Claude Code 项目技能目录结构的测试技能。

## 用途

- 验证 `.claude/skills/test-skill/SKILL.md` 技能文件可被发现和加载
- 作为编写其他项目技能的参考模板

## 使用方式

当用户提到“测试技能”或要求验证技能加载时，按以下步骤执行：

1. 确认当前处于本仓库根目录（存在 `cloud-config-repo/` 目录）
2. 回复：测试技能加载成功
3. 报告当前技能名称：`test-skill`

## 编写新技能的模板

在 `.claude/skills/<技能名>/SKILL.md` 中按以下格式编写：

- YAML frontmatter 包含 `name`（小写字母、数字、连字符，最长 64 字符）和 `description`（第三人称描述用途和触发时机）
- 正文使用 Markdown 写清技能的执行步骤和注意事项
