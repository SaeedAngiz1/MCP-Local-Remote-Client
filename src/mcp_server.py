"""
Main MCP Server Implementation

This module provides the core MCP server functionality,
allowing LLMs to interact with external tools and resources.
"""

import json
import logging
import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server import MCPServer
from mcp.server.stdio import stdio_server
from mcp.types import Tool, Resource

# Import custom tools
from .tools.file_tools import FileTools
from .tools.api_tools import APITools
from .tools.data_tools import DataTools
from .tools.lm_studio_tools import LMStudioTools
from .utils.helpers import setup_logging, load_config

logger = logging.getLogger(__name__)


class MCPServerImpl:
    """
    Main MCP Server implementation
    
    This server provides tools and resources to MCP clients,
    enabling LLMs to interact with external systems.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the MCP server
        
        Args:
            config_path: Path to configuration file
        """
        self.config = load_config(config_path) if config_path else {}
        self.server = MCPServer("mcp-example-server")
        
        # Initialize tools
        self.file_tools = FileTools()
        self.api_tools = APITools()
        self.data_tools = DataTools()
        
        # Initialize LM Studio tools (if enabled)
        lm_studio_config = self.config.get("lm_studio", {})
        if lm_studio_config.get("enabled", False):
            lm_studio_url = lm_studio_config.get("base_url", "http://localhost:1234")
            self.lm_studio = LMStudioTools(base_url=lm_studio_url)
        else:
            self.lm_studio = None
        
        # Setup logging
        log_level = self.config.get("logging", {}).get("level", "INFO")
        setup_logging(log_level)
        
        # Register tools and resources
        self._register_tools()
        self._register_resources()
    
    def _register_tools(self):
        """Register all available tools with the MCP server"""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List all available tools"""
            tools = []
            
            # File tools
            if self._is_tool_enabled("read_file"):
                tools.append(Tool(
                    name="read_file",
                    description="Read content from a file",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to the file to read"
                            }
                        },
                        "required": ["path"]
                    }
                ))
            
            if self._is_tool_enabled("write_file"):
                tools.append(Tool(
                    name="write_file",
                    description="Write content to a file",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to the file to write"
                            },
                            "content": {
                                "type": "string",
                                "description": "Content to write to the file"
                            }
                        },
                        "required": ["path", "content"]
                    }
                ))
            
            if self._is_tool_enabled("list_files"):
                tools.append(Tool(
                    name="list_files",
                    description="List files in a directory",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "directory": {
                                "type": "string",
                                "description": "Directory path to list"
                            }
                        },
                        "required": ["directory"]
                    }
                ))
            
            # API tools
            if self._is_tool_enabled("call_api"):
                tools.append(Tool(
                    name="call_api",
                    description="Make an HTTP API call",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "API endpoint URL"
                            },
                            "method": {
                                "type": "string",
                                "enum": ["GET", "POST", "PUT", "DELETE"],
                                "description": "HTTP method"
                            },
                            "headers": {
                                "type": "object",
                                "description": "HTTP headers"
                            },
                            "body": {
                                "type": "object",
                                "description": "Request body"
                            }
                        },
                        "required": ["url", "method"]
                    }
                ))
            
            # Data tools
            if self._is_tool_enabled("process_data"):
                tools.append(Tool(
                    name="process_data",
                    description="Process and transform data",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "data": {
                                "type": "string",
                                "description": "Data to process (JSON string)"
                            },
                            "operation": {
                                "type": "string",
                                "enum": ["filter", "sort", "transform", "aggregate"],
                                "description": "Operation to perform"
                            }
                        },
                        "required": ["data", "operation"]
                    }
                ))
            
            # LM Studio tools
            if self.lm_studio and self._is_tool_enabled("lm_studio_generate"):
                tools.append(Tool(
                    name="lm_studio_generate",
                    description="Generate text using LM Studio local LLM",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "Input prompt for text generation"
                            },
                            "model": {
                                "type": "string",
                                "description": "Model name (optional, uses default if not specified)"
                            },
                            "max_tokens": {
                                "type": "integer",
                                "description": "Maximum tokens to generate",
                                "default": 100
                            },
                            "temperature": {
                                "type": "number",
                                "description": "Sampling temperature (0.0-1.0)",
                                "default": 0.7
                            }
                        },
                        "required": ["prompt"]
                    }
                ))
            
            if self.lm_studio and self._is_tool_enabled("lm_studio_chat"):
                tools.append(Tool(
                    name="lm_studio_chat",
                    description="Chat completion using LM Studio local LLM",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "messages": {
                                "type": "array",
                                "description": "List of messages with 'role' and 'content'",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "role": {"type": "string", "enum": ["user", "assistant", "system"]},
                                        "content": {"type": "string"}
                                    },
                                    "required": ["role", "content"]
                                }
                            },
                            "model": {
                                "type": "string",
                                "description": "Model name (optional)"
                            },
                            "temperature": {
                                "type": "number",
                                "description": "Sampling temperature",
                                "default": 0.7
                            },
                            "max_tokens": {
                                "type": "integer",
                                "description": "Maximum tokens to generate",
                                "default": 500
                            }
                        },
                        "required": ["messages"]
                    }
                ))
            
            if self.lm_studio and self._is_tool_enabled("lm_studio_list_models"):
                tools.append(Tool(
                    name="lm_studio_list_models",
                    description="List available models in LM Studio",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ))
            
            if self.lm_studio and self._is_tool_enabled("lm_studio_test_connection"):
                tools.append(Tool(
                    name="lm_studio_test_connection",
                    description="Test connection to LM Studio",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ))
            
            return tools
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
            """Execute a tool by name"""
            try:
                if name == "read_file":
                    result = self.file_tools.read_file(arguments["path"])
                    return [{"text": result}]
                
                elif name == "write_file":
                    result = self.file_tools.write_file(
                        arguments["path"],
                        arguments["content"]
                    )
                    return [{"text": f"File written successfully: {result}"}]
                
                elif name == "list_files":
                    result = self.file_tools.list_files(arguments["directory"])
                    return [{"text": json.dumps(result, indent=2)}]
                
                elif name == "call_api":
                    result = await self.api_tools.call_api(
                        url=arguments["url"],
                        method=arguments.get("method", "GET"),
                        headers=arguments.get("headers", {}),
                        body=arguments.get("body")
                    )
                    return [{"text": json.dumps(result, indent=2)}]
                
                elif name == "process_data":
                    result = self.data_tools.process_data(
                        arguments["data"],
                        arguments["operation"]
                    )
                    return [{"text": json.dumps(result, indent=2)}]
                
                # LM Studio tools
                elif name == "lm_studio_generate" and self.lm_studio:
                    result = await self.lm_studio.generate_text(
                        prompt=arguments["prompt"],
                        model=arguments.get("model"),
                        max_tokens=arguments.get("max_tokens", 100),
                        temperature=arguments.get("temperature", 0.7)
                    )
                    return [{"text": f"Generated text:\n{result['text']}\n\nModel: {result['model']}\nTokens used: {result.get('usage', {}).get('total_tokens', 'N/A')}"}]
                
                elif name == "lm_studio_chat" and self.lm_studio:
                    result = await self.lm_studio.chat_completion(
                        messages=arguments["messages"],
                        model=arguments.get("model"),
                        temperature=arguments.get("temperature", 0.7),
                        max_tokens=arguments.get("max_tokens", 500)
                    )
                    message = result.get("message", {})
                    return [{"text": f"Assistant: {message.get('content', '')}\n\nModel: {result.get('model', 'N/A')}"}]
                
                elif name == "lm_studio_list_models" and self.lm_studio:
                    models = await self.lm_studio.list_models()
                    model_list = [m.get("id", "unknown") for m in models]
                    return [{"text": f"Available models in LM Studio:\n{json.dumps(model_list, indent=2)}"}]
                
                elif name == "lm_studio_test_connection" and self.lm_studio:
                    status = await self.lm_studio.test_connection()
                    return [{"text": json.dumps(status, indent=2)}]
                
                else:
                    raise ValueError(f"Unknown tool: {name}")
            
            except Exception as e:
                logger.error(f"Error executing tool {name}: {str(e)}")
                return [{"text": f"Error: {str(e)}", "isError": True}]
    
    def _register_resources(self):
        """Register available resources"""
        
        @self.server.list_resources()
        async def list_resources() -> List[Resource]:
            """List all available resources"""
            resources = []
            
            if self.config.get("resources", {}).get("enabled", False):
                base_path = self.config.get("resources", {}).get("base_path", "./data")
                resources.append(Resource(
                    uri=f"file://{base_path}",
                    name="Data Directory",
                    description="Access to data files",
                    mimeType="application/json"
                ))
            
            return resources
        
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read a resource by URI"""
            try:
                if uri.startswith("file://"):
                    file_path = uri.replace("file://", "")
                    return self.file_tools.read_file(file_path)
                else:
                    raise ValueError(f"Unsupported resource URI: {uri}")
            except Exception as e:
                logger.error(f"Error reading resource {uri}: {str(e)}")
                raise
    
    def _is_tool_enabled(self, tool_name: str) -> bool:
        """Check if a tool is enabled in configuration"""
        enabled_tools = self.config.get("tools", {}).get("enabled", [])
        return tool_name in enabled_tools
    
    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


def main():
    """Main entry point for the MCP server"""
    config_path = "config/mcp_config.json"
    server = MCPServerImpl(config_path)
    
    logger.info("Starting MCP server...")
    asyncio.run(server.run())


if __name__ == "__main__":
    main()

