"""
Model Context Protocol (MCP) Implementation
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .mcp_server import MCPServer
from .utils.helpers import setup_logging

__all__ = ["MCPServer", "setup_logging"]

