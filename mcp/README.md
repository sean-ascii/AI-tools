# MCP 配置

MCP (Model Context Protocol) 服务器配置文件集合。

## 什么是 MCP？

MCP 是一个标准协议，允许 Claude Code 通过插件式的服务器访问外部数据源和工具。

## 通信架构

MCP 支持两种传输类型：

- `stdio`：Claude Code 启动本地子进程，通过标准输入/输出通信
- `http`：Claude Code 直接通过 HTTP 与远程 MCP 服务通信

## 配置文件位置

MCP 配置统一存储在 `~/.claude.json` 的 `mcpServers` 字段中，例如：

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_GITHUB_TOKEN"
      }
    }
  }
}
```

## 可用的 MCP 配置

### github-mcp.json

GitHub 集成，提供仓库、Issue、PR 等操作能力。使用 HTTP 类型直连 GitHub Copilot MCP 服务。

**安装步骤**：

1. 获取 GitHub Personal Access Token
   - 访问 https://github.com/settings/tokens
   - 创建新 token，授予必要权限（repo、read:org 等）

2. 运行安装命令（推荐，不易出错）：

   ```bash
   claude mcp add-json github --scope user '{"type":"http","url":"https://api.githubcopilot.com/mcp","headers":{"Authorization":"Bearer YOUR_GITHUB_TOKEN"}}'
   ```

   将 `YOUR_GITHUB_TOKEN` 替换为你的实际 token。

3. 重启 Claude Code 使配置生效

> 也可以手动将 [github-mcp.json](github-mcp.json) 中的内容合并到 `~/.claude.json` 的 `mcpServers` 字段，效果一致。可参考该文件校验配置是否完整。

**使用方式**：

配置完成后，Claude Code 会自动加载 GitHub MCP 服务器，你可以直接请求：
- "查看我的 GitHub 仓库"
- "创建一个 Issue"
- "查看最近的 PR"

## 添加新的 MCP 服务器

**stdio 类型**（本地子进程）：

```bash
claude mcp add <name> --scope user -- <command> [args...]
```

**http 类型**（远程服务）：

```bash
claude mcp add-json <name> --scope user '{"type":"http","url":"<url>","headers":{"Authorization":"Bearer <token>"}}'
```

**手动方式**：直接编辑 `~/.claude.json` 的 `mcpServers` 字段，效果一致。

建议在此目录保存对应的配置文件（如 `custom-mcp.json`）作为参考，方便校验和迁移。

## 常见问题

**Q: MCP 服务器无法启动？**

- 检查 token 是否有效且权限足够
- 检查 `command` 是否正确安装（stdio 类型需要 Node.js 等依赖）
- 查看 Claude Code 日志获取详细错误信息

## 参考资源

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [GitHub MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/github)
