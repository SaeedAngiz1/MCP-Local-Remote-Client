# MCP Project Setup - Windows CMD Guide

This guide provides **Windows CMD (Command Prompt)** commands for setting up the MCP project. You don't need PowerShell!

## Step 1: Create Project Directories

Open **Command Prompt (CMD)** and run:

```cmd
mkdir src\tools
mkdir src\utils
mkdir examples
mkdir tests
mkdir docs
mkdir config
mkdir data
mkdir logs
```

Or create them all at once (CMD will create parent directories automatically):

```cmd
mkdir src\tools src\utils examples tests docs config data logs
```

## Step 2: Create Virtual Environment

```cmd
python -m venv venv
```

## Step 3: Activate Virtual Environment

```cmd
venv\Scripts\activate.bat
```

**Note**: After activation, your prompt should show `(venv)` at the beginning.

## Step 4: Install Dependencies

```cmd
pip install -r requirements.txt
```

## Step 5: Verify Installation

```cmd
python -c "import mcp; print('MCP installed successfully!')"
```

## Step 6: Run Examples

```cmd
python examples\basic_server.py
```

## Common CMD Commands for This Project

### Navigate to Project Directory
```cmd
cd C:\Users\angiz\OneDrive\Desktop\cursor
```

### List Files
```cmd
dir
```

### List Files in Directory
```cmd
dir src
```

### Create a File (using echo)
```cmd
echo. > filename.txt
```

### View File Contents
```cmd
type filename.txt
```

### Check Python Version
```cmd
python --version
```

### Check if Virtual Environment is Active
```cmd
echo %VIRTUAL_ENV%
```
(Should show the path to venv if active)

### Deactivate Virtual Environment
```cmd
deactivate
```

### Run Tests
```cmd
python -m pytest tests\
```

### Run with Coverage
```cmd
python -m pytest --cov=src tests\
```

## Troubleshooting CMD Issues

### Issue: "python is not recognized"
**Solution**: 
- Make sure Python is installed
- Add Python to PATH, or use full path: `C:\Python3x\python.exe -m venv venv`

### Issue: "pip is not recognized"
**Solution**:
- Use: `python -m pip install -r requirements.txt`

### Issue: Virtual Environment Won't Activate
**Solution**:
- Make sure you're in the project directory
- Use: `venv\Scripts\activate.bat` (not `activate` or `activate.ps1`)

### Issue: Paths with Spaces
**Solution**:
- Use quotes: `cd "C:\Users\angiz\OneDrive\Desktop\cursor"`

## All Setup Steps in CMD

Here's the complete setup sequence for CMD:

```cmd
REM 1. Navigate to project directory
cd C:\Users\angiz\OneDrive\Desktop\cursor

REM 2. Create directories
mkdir src\tools
mkdir src\utils
mkdir examples
mkdir tests
mkdir docs
mkdir config
mkdir data
mkdir logs

REM 3. Create virtual environment
python -m venv venv

REM 4. Activate virtual environment
venv\Scripts\activate.bat

REM 5. Install dependencies
pip install -r requirements.txt

REM 6. Verify installation
python -c "import mcp; print('MCP installed!')"

REM 7. Run example (in another CMD window)
python examples\basic_server.py
```

## Differences: CMD vs PowerShell

| Task | CMD | PowerShell |
|------|-----|------------|
| Create directory | `mkdir dirname` | `mkdir dirname` or `New-Item -ItemType Directory` |
| Activate venv | `venv\Scripts\activate.bat` | `venv\Scripts\Activate.ps1` |
| Path separator | `\` (backslash) | `\` or `/` |
| List files | `dir` | `dir` or `Get-ChildItem` |
| View file | `type filename` | `Get-Content filename` or `cat filename` |

## Important Notes

1. **Always use backslashes (`\`) in paths** for CMD
2. **Activate venv with `.bat` file**, not `.ps1`
3. **Use `python -m` prefix** for modules (e.g., `python -m pip`, `python -m pytest`)
4. **Quotes are needed** for paths with spaces

## Quick Reference Card

```cmd
REM Setup
cd your\project\path
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt

REM Development
python src\mcp_server.py
python examples\basic_server.py
python -m pytest tests\

REM Deactivate
deactivate
```

---

**You can use CMD for everything!** No PowerShell required. 🎉

