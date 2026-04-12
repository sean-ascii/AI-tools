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

## Skills

### code-commit
创建带上下文的 Git 提交，自动生成符合 conventional commits 规范的提交信息。

### code-review
提供全面的代码审查能力，覆盖安全、性能和代码质量分析。

### code-optimize
分析代码中的性能问题并提出优化建议。

## Hooks

### pre-bash-safety-check.sh
在执行 Bash 命令前进行安全检查，阻止或警告潜在的危险命令（如 `rm -rf /`、`git push --force` 等）。

## MCP 配置

### github
GitHub 集成，提供仓库、Issue、PR 等操作能力。使用 HTTP 类型直连 GitHub Copilot MCP 服务。

```bash
claude mcp add-json github --scope user '{"type":"http","url":"https://api.githubcopilot.com/mcp","headers":{"Authorization":"Bearer YOUR_GITHUB_TOKEN"}}'
```

详见 [mcp/README.md](mcp/README.md)。

## 使用方法

**Skills**：将 skills 目录下的技能复制到 `~/.claude/skills/`

**Hooks**：将 hooks 目录下的钩子复制到 `~/.claude/hooks/` 并添加执行权限，然后在 `~/.claude/settings.json` 中配置：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "~/.claude/hooks/pre-bash-safety-check.sh" }]
      }
    ]
  }
}
```

**MCP**：使用 `claude mcp add` 命令安装，详见 [mcp/README.md](mcp/README.md)。

## 许可

个人使用项目
