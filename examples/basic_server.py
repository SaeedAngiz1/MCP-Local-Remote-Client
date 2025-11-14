"""
Basic MCP Server Example

This is a minimal example showing how to create and run an MCP server.
"""

import asyncio
import logging
from mcp.server import MCPServer
from mcp.server.stdio import stdio_server
from mcp import Tool

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create server instance
server = MCPServer("basic-mcp-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="greet",
            description="Greet someone by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the person to greet"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="add_numbers",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[dict]:
    """Handle tool calls"""
    try:
        if name == "greet":
            name_arg = arguments.get("name", "World")
            message = f"Hello, {name_arg}!"
            return [{"text": message}]
        
        elif name == "add_numbers":
            a = arguments.get("a", 0)
            b = arguments.get("b", 0)
            result = a + b
            return [{"text": f"{a} + {b} = {result}"}]
        
        else:
            return [{"text": f"Unknown tool: {name}", "isError": True}]
    
    except Exception as e:
        logger.error(f"Error executing tool {name}: {str(e)}")
        return [{"text": f"Error: {str(e)}", "isError": True}]


async def main():
    """Main entry point"""
    logger.info("Starting basic MCP server...")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

