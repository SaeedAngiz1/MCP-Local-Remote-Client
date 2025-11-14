# MCP Tutorial: Step-by-Step Guide

This tutorial will walk you through creating and using an MCP (Model Context Protocol) implementation from scratch.

## Prerequisites

Before starting, ensure you have:
- Python 3.9 or higher installed
- Basic understanding of Python
- Familiarity with async/await (helpful but not required)

## Step 1: Project Setup

### 1.1 Create Project Directory

```bash
mkdir mcp-project
cd mcp-project
```

### 1.2 Initialize Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 1.3 Install Dependencies

```bash
pip install mcp fastapi uvicorn httpx
```

## Step 2: Create Basic MCP Server

### 2.1 Create Server File

Create `server.py`:

```python
import asyncio
from mcp.server import MCPServer
from mcp.server.stdio import stdio_server
from mcp import Tool

server = MCPServer("my-mcp-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="hello",
            description="Say hello",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "hello":
        name = arguments.get("name", "World")
        return [{"text": f"Hello, {name}!"}]
    return [{"text": f"Unknown tool: {name}"}]

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

### 2.2 Test the Server

Run the server:

```bash
python server.py
```

## Step 3: Add File Tools

### 3.1 Create File Tools Module

Create `tools.py`:

```python
from pathlib import Path

class FileTools:
    def read_file(self, path: str) -> str:
        with open(path, 'r') as f:
            return f.read()
    
    def write_file(self, path: str, content: str) -> str:
        with open(path, 'w') as f:
            f.write(content)
        return f"Wrote to {path}"
```

### 3.2 Integrate into Server

Update `server.py` to include file tools:

```python
from tools import FileTools

file_tools = FileTools()

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # ... existing tools ...
        Tool(
            name="read_file",
            description="Read a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    # ... existing handlers ...
    if name == "read_file":
        content = file_tools.read_file(arguments["path"])
        return [{"text": content}]
```

## Step 4: Add API Tools

### 4.1 Create API Tools

Add to `tools.py`:

```python
import httpx

class APITools:
    async def call_api(self, url: str, method: str = "GET"):
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url)
            return {
                "status": response.status_code,
                "data": response.json()
            }
```

### 4.2 Register API Tool

Add the API tool to your server's tool list and handler.

## Step 5: Create MCP Client

### 5.1 Create Client File

Create `client.py`:

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List tools
            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools])
            
            # Call a tool
            result = await session.call_tool("hello", {"name": "MCP"})
            print("Result:", result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())
```

## Step 6: Add Configuration

### 6.1 Create Config File

Create `config.json`:

```json
{
  "server": {
    "name": "My MCP Server",
    "port": 8000
  },
  "tools": {
    "enabled": ["read_file", "write_file", "call_api"]
  }
}
```

### 6.2 Load Configuration

Update server to load config:

```python
import json

with open("config.json") as f:
    config = json.load(f)
```

## Step 7: Add Error Handling

### 7.1 Improve Error Handling

Update tool handlers:

```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        # Tool execution
        ...
    except FileNotFoundError:
        return [{"text": "File not found", "isError": True}]
    except Exception as e:
        return [{"text": f"Error: {str(e)}", "isError": True}]
```

## Step 8: Add Logging

### 8.1 Setup Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

### 8.2 Add Log Statements

```python
logger.info(f"Tool called: {name}")
logger.error(f"Error: {str(e)}")
```

## Step 9: Testing

### 9.1 Write Tests

Create `test_server.py`:

```python
import pytest
from tools import FileTools

def test_read_file():
    tools = FileTools()
    content = tools.read_file("test.txt")
    assert content == "expected content"
```

### 9.2 Run Tests

```bash
pytest test_server.py
```

## Step 10: Documentation

### 10.1 Create README

Document your project:
- Installation instructions
- Usage examples
- API documentation
- Contributing guidelines

### 10.2 Add Docstrings

Document all functions:

```python
def read_file(self, path: str) -> str:
    """
    Read content from a file.
    
    Args:
        path: Path to the file
        
    Returns:
        File content as string
    """
    ...
```

## Next Steps

1. **Add More Tools**: Implement additional tools for your use case
2. **Add Resources**: Expose data sources as resources
3. **Improve Security**: Add authentication and validation
4. **Add Monitoring**: Implement metrics and observability
5. **Deploy**: Set up deployment for production use

## Common Patterns

### Pattern 1: Tool with Validation

```python
def validate_input(arguments: dict, required: list):
    for field in required:
        if field not in arguments:
            raise ValueError(f"Missing required field: {field}")

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    validate_input(arguments, ["path"])
    # ... tool logic
```

### Pattern 2: Async Tool

```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "async_operation":
        result = await some_async_function(arguments)
        return [{"text": result}]
```

### Pattern 3: Resource Access

```python
@server.list_resources()
async def list_resources():
    return [
        Resource(
            uri="file://data.json",
            name="Data File",
            mimeType="application/json"
        )
    ]

@server.read_resource()
async def read_resource(uri: str):
    if uri.startswith("file://"):
        path = uri.replace("file://", "")
        return read_file(path)
```

## Troubleshooting

### Issue: Server not starting
- Check Python version (3.9+)
- Verify dependencies installed
- Check for syntax errors

### Issue: Tools not appearing
- Verify tool registration
- Check tool schema format
- Review server logs

### Issue: Tool execution fails
- Validate input arguments
- Check error handling
- Review tool implementation

## Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [MCP GitHub](https://github.com/modelcontextprotocol)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

Happy coding with MCP! 🚀

