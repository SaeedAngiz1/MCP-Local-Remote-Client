"""
Utility helper functions for MCP implementation
"""

import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional


def setup_logging(level: str = "INFO", log_file: Optional[str] = None):
    """
    Setup logging configuration
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
    """
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # File handler (if specified)
    handlers = [console_handler]
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        handlers=handlers
    )


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from JSON file
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    try:
        config_file = Path(config_path)
        if not config_file.exists():
            logging.warning(f"Config file not found: {config_path}, using defaults")
            return {}
        
        with open(config_file, 'r') as f:
            return json.load(f)
    
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing config file: {e}")
        return {}
    except Exception as e:
        logging.error(f"Error loading config file: {e}")
        return {}


def validate_tool_input(tool_name: str, arguments: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """
    Validate tool input against schema
    
    Args:
        tool_name: Name of the tool
        arguments: Tool arguments
        schema: JSON schema for validation
        
    Returns:
        True if valid, False otherwise
    """
    required = schema.get("properties", {}).get("required", [])
    
    for field in required:
        if field not in arguments:
            logging.error(f"Missing required field '{field}' for tool '{tool_name}'")
            return False
    
    return True

