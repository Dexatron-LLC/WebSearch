# Web Navigator MCP

Simple MCP server for web navigation using Playwright.

## Setup

```bash
uv sync
uv run playwright install chromium
```

## Usage

Run the server:
```bash
uv run python server.py
```

## Claude Code Configuration

Add to your `~/.claude/claude_code_config.json`:

```json
{
  "mcpServers": {
    "web-navigator": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/path/to/web-navigator-mcp"
    }
  }
}
```

## Tools

- `navigate` - Navigate to a URL
- `get_content` - Get page text content
- `get_html` - Get page HTML
- `screenshot` - Take a screenshot
- `click` - Click element by CSS selector
- `fill` - Fill form field by CSS selector
