"""Simple MCP server for web navigation using Playwright."""

import asyncio
import base64
from contextlib import asynccontextmanager
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent
from playwright.async_api import async_playwright, Browser, Page

server = Server("web-navigator")

# Global state
browser: Browser | None = None
page: Page | None = None
playwright_instance = None


async def get_page() -> Page:
    """Get or create a browser page."""
    global browser, page, playwright_instance

    if page is None or page.is_closed():
        if playwright_instance is None:
            playwright_instance = await async_playwright().start()
        if browser is None:
            browser = await playwright_instance.chromium.launch(headless=True)
        page = await browser.new_page()

    return page


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="navigate",
            description="Navigate to a URL",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL to navigate to"}
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="get_content",
            description="Get the text content of the current page",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="screenshot",
            description="Take a screenshot of the current page",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="click",
            description="Click on an element by CSS selector",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {"type": "string", "description": "CSS selector of element to click"}
                },
                "required": ["selector"]
            }
        ),
        Tool(
            name="fill",
            description="Fill a form field with text",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {"type": "string", "description": "CSS selector of input field"},
                    "value": {"type": "string", "description": "Text to fill in"}
                },
                "required": ["selector", "value"]
            }
        ),
        Tool(
            name="get_html",
            description="Get the HTML content of the current page",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_element_text",
            description="Get the text content of an element by CSS selector",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {"type": "string", "description": "CSS selector of element"}
                },
                "required": ["selector"]
            }
        ),
        Tool(
            name="get_element_html",
            description="Get the inner HTML of an element by CSS selector",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector": {"type": "string", "description": "CSS selector of element"}
                },
                "required": ["selector"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent]:
    """Handle tool calls."""
    p = await get_page()

    if name == "navigate":
        url = arguments["url"]
        await p.goto(url)
        return [TextContent(type="text", text=f"Navigated to {url}. Title: {await p.title()}")]

    elif name == "get_content":
        content = await p.inner_text("body")
        return [TextContent(type="text", text=content[:10000])]  # Limit content size

    elif name == "screenshot":
        screenshot_bytes = await p.screenshot()
        b64 = base64.standard_b64encode(screenshot_bytes).decode("utf-8")
        return [ImageContent(type="image", data=b64, mimeType="image/png")]

    elif name == "click":
        selector = arguments["selector"]
        await p.click(selector)
        return [TextContent(type="text", text=f"Clicked on {selector}")]

    elif name == "fill":
        selector = arguments["selector"]
        value = arguments["value"]
        await p.fill(selector, value)
        return [TextContent(type="text", text=f"Filled {selector} with text")]

    elif name == "get_html":
        html = await p.content()
        return [TextContent(type="text", text=html[:10000])]  # Limit content size

    elif name == "get_element_text":
        selector = arguments["selector"]
        content = await p.inner_text(selector)
        return [TextContent(type="text", text=content[:10000])]

    elif name == "get_element_html":
        selector = arguments["selector"]
        html = await p.inner_html(selector)
        return [TextContent(type="text", text=html[:10000])]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def cleanup():
    """Clean up browser resources."""
    global browser, playwright_instance
    if browser:
        await browser.close()
    if playwright_instance:
        await playwright_instance.stop()


async def async_main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        try:
            await server.run(read_stream, write_stream, server.create_initialization_options())
        finally:
            await cleanup()


def main():
    """Entry point for the MCP server."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
