"""
Custom Tools Example

This example demonstrates how to create custom MCP tools.
"""

import asyncio
import logging
from mcp.server import MCPServer
from mcp.server.stdio import stdio_server
from mcp import Tool
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server = MCPServer("custom-tools-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List custom tools"""
    return [
        Tool(
            name="get_current_time",
            description="Get the current date and time",
            inputSchema={
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "enum": ["iso", "unix", "readable"],
                        "description": "Time format"
                    }
                }
            }
        ),
        Tool(
            name="calculate",
            description="Perform mathematical calculations",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression (e.g., '2 + 2', '10 * 5')"
                    }
                },
                "required": ["expression"]
            }
        ),
        Tool(
            name="text_analysis",
            description="Analyze text and provide statistics",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to analyze"
                    }
                },
                "required": ["text"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[dict]:
    """Handle custom tool calls"""
    try:
        if name == "get_current_time":
            format_type = arguments.get("format", "iso")
            now = datetime.now()
            
            if format_type == "iso":
                result = now.isoformat()
            elif format_type == "unix":
                result = str(int(now.timestamp()))
            else:  # readable
                result = now.strftime("%Y-%m-%d %H:%M:%S")
            
            return [{"text": f"Current time: {result}"}]
        
        elif name == "calculate":
            expression = arguments.get("expression", "")
            try:
                # Simple and safe evaluation (in production, use a proper math parser)
                # This is a simplified example - be careful with eval in production!
                result = eval(expression, {"__builtins__": {}}, {})
                return [{"text": f"{expression} = {result}"}]
            except Exception as e:
                return [{"text": f"Error calculating: {str(e)}", "isError": True}]
        
        elif name == "text_analysis":
            text = arguments.get("text", "")
            words = text.split()
            chars = len(text)
            chars_no_spaces = len(text.replace(" ", ""))
            sentences = text.count(".") + text.count("!") + text.count("?")
            
            analysis = {
                "character_count": chars,
                "character_count_no_spaces": chars_no_spaces,
                "word_count": len(words),
                "sentence_count": sentences,
                "average_word_length": sum(len(w) for w in words) / len(words) if words else 0
            }
            
            result_text = "\n".join([f"{k}: {v}" for k, v in analysis.items()])
            return [{"text": f"Text Analysis:\n{result_text}"}]
        
        else:
            return [{"text": f"Unknown tool: {name}", "isError": True}]
    
    except Exception as e:
        logger.error(f"Error executing tool {name}: {str(e)}")
        return [{"text": f"Error: {str(e)}", "isError": True}]


async def main():
    """Main entry point"""
    logger.info("Starting custom tools MCP server...")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

