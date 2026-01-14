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

### Using from GitHub (no clone required)

Add to your `~/.claude/claude_code_config.json`:

```json
{
  "mcpServers": {
    "web-navigator": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/Dexatron-LLC/WebSearch", "web-navigator-mcp"]
    }
  }
}
```

Note: You'll need to install Playwright's Chromium browser once:
```bash
uvx --from git+https://github.com/Dexatron-LLC/WebSearch playwright install chromium
```

### Using from local clone

Add to your `~/.claude/claude_code_config.json`:

```json
{
  "mcpServers": {
    "web-navigator": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/path/to/WebSearch"
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
