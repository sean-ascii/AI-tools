# AI Tools

个人常用的 AI 技能和自动化流程集合，用于提升开发效率和代码质量。

## 项目结构

```
AI-tools/
├── skills/          # Claude Code 自定义技能
├── hooks/           # Git 和工具执行钩子
├── subagents/       # 子代理配置
├── plugins/         # 插件扩展
├── mcp/             # MCP (Model Context Protocol) 配置
└── memory/          # 项目记忆和上下文
```

## 技能列表

### code-commit
创建带上下文的 Git 提交，自动生成符合 conventional commits 规范的提交信息。

### code-review
提供全面的代码审查能力，覆盖安全、性能和代码质量分析。

### code-optimize
分析代码中的性能问题并提出优化建议。

## Hooks

### pre-bash-safety-check.sh
在执行 Bash 命令前进行安全检查，阻止或警告潜在的危险命令（如 `rm -rf /`、`git push --force` 等）。

## 使用方法

1. 将 skills 目录下的技能复制到 `~/.claude/skills/`
2. 将 hooks 目录下的钩子复制到 `~/.claude/hooks/` 并添加执行权限
3. 根据需要在 `~/.claude/settings.json` 中配置相应的钩子

## 许可

个人使用项目
