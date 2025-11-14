# Contributing to MCP Project

Thank you for your interest in contributing to this MCP (Model Context Protocol) project! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)
- Any relevant error messages or logs

### Suggesting Features

Feature suggestions are welcome! Please open an issue with:
- A clear description of the feature
- Use cases and examples
- Potential implementation approach (if you have ideas)

### Submitting Code

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow the code style (see below)
   - Add tests for new features
   - Update documentation as needed
4. **Test your changes**
   ```bash
   pytest tests/
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add: description of your changes"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request**

## Code Style

- Follow PEP 8 for Python code
- Use type hints where possible
- Add docstrings to all functions and classes
- Keep functions focused and small
- Use meaningful variable and function names

### Example

```python
def read_file(self, file_path: str) -> str:
    """
    Read content from a file.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        File content as string
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    with open(file_path, 'r') as f:
        return f.read()
```

## Testing

- Write tests for all new features
- Ensure all existing tests pass
- Aim for good test coverage
- Use descriptive test names

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_mcp_server.py
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to all new functions/classes
- Update examples if API changes
- Keep architecture docs up to date

## Project Structure

```
mcp-project/
├── src/           # Main source code
├── examples/      # Example implementations
├── tests/         # Test files
├── docs/          # Documentation
└── config/        # Configuration files
```

## Commit Messages

Use clear, descriptive commit messages:

- `Add: new feature description`
- `Fix: bug description`
- `Update: what was updated`
- `Refactor: what was refactored`
- `Docs: documentation changes`

## Pull Request Process

1. Ensure your code follows the style guidelines
2. All tests must pass
3. Update documentation as needed
4. Request review from maintainers
5. Address any feedback
6. Once approved, maintainers will merge

## Questions?

Feel free to:
- Open an issue for questions
- Check existing issues and PRs
- Review the documentation

Thank you for contributing! 🎉

