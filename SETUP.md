# Quick Setup Guide

This guide will help you get your MCP project up and running quickly.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git (optional, for version control)

## Installation Steps

### 1. Clone or Download the Project

```bash
# If using Git
git clone <your-repo-url>
cd mcp-project

# Or download and extract the ZIP file
```

### 2. Create Virtual Environment

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

### 3. Install Dependencies

**Windows CMD/PowerShell:**
```cmd
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
pip install -r requirements.txt
```

### 4. Verify Installation

**Windows CMD/PowerShell:**
```cmd
python -c "import mcp; print('MCP installed successfully!')"
```

**macOS/Linux:**
```bash
python3 -c "import mcp; print('MCP installed successfully!')"
```

### 5. Run Example Server

**Windows CMD:**
```cmd
REM Basic example
python examples\basic_server.py

REM Full server
python src\mcp_server.py
```

**macOS/Linux:**
```bash
# Basic example
python examples/basic_server.py

# Full server
python src/mcp_server.py
```

### 6. Test with Client

In another terminal:

**Windows CMD:**
```cmd
python examples\client_example.py
```

**macOS/Linux:**
```bash
python examples/client_example.py
```

## Troubleshooting

### Issue: `mcp` module not found

**Solution**: Make sure you've activated your virtual environment and installed dependencies:
```bash
pip install mcp
```

### Issue: Import errors

**Solution**: Ensure you're running from the project root directory:
```bash
cd /path/to/mcp-project
python examples/basic_server.py
```

### Issue: Permission errors (macOS/Linux)

**Solution**: You may need to use `python3` instead of `python`:
```bash
python3 -m venv venv
python3 examples/basic_server.py
```

### Issue: Using Windows CMD instead of PowerShell

**Solution**: See [SETUP_CMD.md](SETUP_CMD.md) for a complete CMD-specific guide. Key differences:
- Use `venv\Scripts\activate.bat` (not `.ps1`)
- Use backslashes `\` in paths
- Commands work the same otherwise

## Next Steps

1. Read the [README.md](README.md) for detailed documentation
2. Check out [docs/TUTORIAL.md](docs/TUTORIAL.md) for step-by-step guide
3. Explore [examples/](examples/) for code examples
4. Review [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for architecture details

## Getting Help

- Check the [MCP Documentation](https://modelcontextprotocol.io)
- Review example code in the `examples/` directory
- Open an issue on GitHub if you encounter problems

---

Happy coding! 🚀

