"""
MCP Client Example

This example shows how to connect to and interact with an MCP server.
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Example client usage"""
    
    # Configure server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["examples/basic_server.py"]
    )
    
    # Connect to server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            # List available tools
            print("Available tools:")
            tools = await session.list_tools()
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Call a tool
            print("\nCalling 'greet' tool:")
            result = await session.call_tool("greet", {"name": "MCP User"})
            print(f"Result: {result.content[0].text}")
            
            # Call another tool
            print("\nCalling 'add_numbers' tool:")
            result = await session.call_tool("add_numbers", {"a": 5, "b": 3})
            print(f"Result: {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())

