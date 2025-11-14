# Model Context Protocol (MCP) Project

A comprehensive implementation of the Model Context Protocol (MCP) - an open standard for connecting AI systems, particularly Large Language Models (LLMs), with external tools, services, and data sources.

## 📋 Table of Contents

- [What is MCP?](#what-is-mcp)
- [Project Structure](#project-structure)
- [Step-by-Step Setup Guide](#step-by-step-setup-guide)
- [Features](#features)
- [Usage](#usage)
- [Examples](#examples)
- [Architecture](#architecture)
- [Integrations](#-integrations)
- [Resources](#-resources)
- [Contributing](#contributing)
- [License](#license)

## 🎯 What is MCP?

The Model Context Protocol (MCP) is an open standard introduced by Anthropic that standardizes the integration of AI systems with external tools and data sources. It provides:

- **Universal Interface**: For reading files, executing functions, and handling contextual prompts
- **Client-Server Architecture**: Enables secure, bidirectional communication
- **Tool Integration**: Connect LLMs to databases, APIs, file systems, and more
- **Context Management**: Structured way to provide context to AI models

## 📁 Project Structure

```
mcp-project/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── config/
│   └── mcp_config.json      # MCP server configuration
├── src/
│   ├── __init__.py
│   ├── mcp_server.py        # Main MCP server implementation
│   ├── tools/               # Custom MCP tools
│   │   ├── __init__.py
│   │   ├── file_tools.py   # File system operations
│   │   ├── api_tools.py    # API integration tools
│   │   └── data_tools.py   # Data processing tools
│   └── utils/
│       ├── __init__.py
│       └── helpers.py      # Utility functions
├── examples/
│   ├── basic_server.py     # Basic MCP server example
│   ├── client_example.py   # MCP client example
│   └── custom_tools.py     # Custom tools example
├── tests/
│   ├── __init__.py
│   └── test_mcp_server.py  # Unit tests
└── docs/
    ├── ARCHITECTURE.md     # Architecture documentation
    └── TUTORIAL.md         # Detailed tutorial
```

## 🚀 Step-by-Step Setup Guide

> **💡 Windows CMD Users**: See [SETUP_CMD.md](SETUP_CMD.md) for a complete CMD-specific guide with all commands.

### Step 1: Prerequisites

Ensure you have the following installed:
- Python 3.9 or higher
- pip (Python package manager)
- Git

### Step 2: Clone or Initialize the Repository

**Windows CMD:**
```cmd
mkdir mcp-project
cd mcp-project
git init
```

**macOS/Linux:**
```bash
mkdir mcp-project
cd mcp-project
git init
```

### Step 3: Create Virtual Environment

**Windows CMD:**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Windows PowerShell:**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

**Windows CMD/PowerShell:**
```cmd
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
pip install -r requirements.txt
```

### Step 5: Install MCP SDK

```bash
# Install the official MCP Python SDK
pip install mcp

# Or install from source
pip install git+https://github.com/modelcontextprotocol/python-sdk.git
```

### Step 6: Configure MCP Server

1. Edit `config/mcp_config.json` to configure your server settings
2. Define your tools and resources
3. Set up authentication if needed

### Step 7: Run the Example Server

**Windows CMD:**
```cmd
REM Run the basic example
python examples\basic_server.py

REM Or run the full server
python src\mcp_server.py
```

**macOS/Linux:**
```bash
# Run the basic example
python examples/basic_server.py

# Or run the full server
python src/mcp_server.py
```

### Step 8: Test the Implementation

**Windows CMD:**
```cmd
REM Run tests
python -m pytest tests\

REM Or run manually
python examples\client_example.py
```

**macOS/Linux:**
```bash
# Run tests
pytest tests/

# Or run manually
python examples/client_example.py
```

## ✨ Features

- ✅ **MCP Server Implementation**: Full-featured MCP server with tool support
- ✅ **Custom Tools**: Examples of file operations, API calls, and data processing
- ✅ **Client Integration**: Example client for connecting to MCP servers
- ✅ **Configuration Management**: JSON-based configuration system
- ✅ **Error Handling**: Robust error handling and logging
- ✅ **Type Safety**: Type hints throughout the codebase
- ✅ **Testing**: Unit tests for core functionality

## 📖 Usage

### Starting an MCP Server

```python
from src.mcp_server import MCPServer

# Initialize server
server = MCPServer(config_path="config/mcp_config.json")

# Start server
server.start()
```

### Using MCP Tools

```python
from src.tools.file_tools import FileTools

# Initialize file tools
file_tools = FileTools()

# Read a file
content = file_tools.read_file("path/to/file.txt")

# Write to a file
file_tools.write_file("path/to/file.txt", "content")
```

### Client Connection

```python
from src.mcp_client import MCPClient

# Connect to MCP server
client = MCPClient(server_url="http://localhost:8000")

# Call a tool
result = client.call_tool("read_file", {"path": "example.txt"})
```

## 🎓 Examples

See the `examples/` directory for:
- **basic_server.py**: Minimal MCP server implementation
- **client_example.py**: How to connect and use an MCP server
- **custom_tools.py**: Creating custom MCP tools

## 🏗️ Architecture

MCP follows a client-server architecture:

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   LLM App   │◄───────►│ MCP Client  │◄───────►│ MCP Server  │
│  (Claude)   │         │             │         │             │
└─────────────┘         └─────────────┘         └──────┬──────┘
                                                        │
                                                ┌────────┴────────┐
                                                │                 │
                                         ┌──────▼──────┐  ┌──────▼──────┐
                                         │   Tools     │  │  Resources  │
                                         │  (Actions)  │  │   (Data)    │
                                         └─────────────┘  └─────────────┘
```

### Key Components:

1. **MCP Server**: Provides tools and resources to clients
2. **MCP Client**: Connects to servers and makes requests
3. **Tools**: Executable functions (e.g., read_file, call_api)
4. **Resources**: Data sources (e.g., files, databases)

## 🔧 Development

### Adding Custom Tools

1. Create a new file in `src/tools/`
2. Implement tool functions following the MCP tool interface
3. Register tools in `mcp_server.py`

Example:
```python
from mcp import Tool

@Tool(name="my_custom_tool", description="Does something custom")
def my_custom_tool(param: str) -> str:
    # Your implementation
    return result
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/
```

## 🔌 Integrations

This project includes comprehensive integration guides for popular tools and services:

- **[INTEGRATIONS.md](INTEGRATIONS.md)** - Complete guide for integrating with:
  - LM Studio
  - Docker Desktop
  - Obsidian (Local REST API & Marcel Marais' server)
  - Logseq
  - Cursor IDE
  - Claude Sonnet
  - Cloud Server Setup

- **[CURSOR_LM_STUDIO_SETUP.md](CURSOR_LM_STUDIO_SETUP.md)** - Quick setup guide for:
  - Connecting LM Studio with Cursor
  - Testing the connection
  - Using LM Studio tools in Cursor
  - **Remote access via iPhone A-Shell and Tailscale**
  - Troubleshooting common issues

- **[REMOTE_ACCESS.md](REMOTE_ACCESS.md)** - Guide for remote access:
  - Accessing LM Studio from iPhone/Android
  - Tailscale setup and configuration
  - A-Shell (iOS) and Termux (Android) usage
  - SSH tunneling methods
  - Security best practices

## 📚 Resources

- [MCP Official Documentation](https://modelcontextprotocol.io)
- [MCP GitHub Repository](https://github.com/modelcontextprotocol)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Specification](https://spec.modelcontextprotocol.io)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Anthropic for creating the Model Context Protocol
- The MCP community for their contributions and support

---

**Made with ❤️ for the MCP community**

