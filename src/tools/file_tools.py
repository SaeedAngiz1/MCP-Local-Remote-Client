"""
File System Tools for MCP

Provides tools for reading, writing, and managing files.
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class FileTools:
    """Tools for file system operations"""
    
    def __init__(self, base_path: str = "."):
        """
        Initialize file tools
        
        Args:
            base_path: Base directory for file operations
        """
        self.base_path = Path(base_path).resolve()
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def read_file(self, file_path: str) -> str:
        """
        Read content from a file
        
        Args:
            file_path: Path to the file (relative to base_path)
            
        Returns:
            File content as string
            
        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file cannot be read
        """
        try:
            full_path = self.base_path / file_path
            # Security: Ensure path is within base_path
            if not str(full_path.resolve()).startswith(str(self.base_path.resolve())):
                raise ValueError("Path outside allowed directory")
            
            if not full_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"Read file: {file_path}")
            return content
        
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            raise
    
    def write_file(self, file_path: str, content: str) -> str:
        """
        Write content to a file
        
        Args:
            file_path: Path to the file (relative to base_path)
            content: Content to write
            
        Returns:
            Success message
        """
        try:
            full_path = self.base_path / file_path
            # Security: Ensure path is within base_path
            if not str(full_path.resolve()).startswith(str(self.base_path.resolve())):
                raise ValueError("Path outside allowed directory")
            
            # Create parent directories if needed
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Wrote file: {file_path}")
            return f"Successfully wrote to {file_path}"
        
        except Exception as e:
            logger.error(f"Error writing file {file_path}: {str(e)}")
            raise
    
    def list_files(self, directory: str = ".") -> List[Dict[str, Any]]:
        """
        List files in a directory
        
        Args:
            directory: Directory path (relative to base_path)
            
        Returns:
            List of file information dictionaries
        """
        try:
            full_path = self.base_path / directory
            # Security: Ensure path is within base_path
            if not str(full_path.resolve()).startswith(str(self.base_path.resolve())):
                raise ValueError("Path outside allowed directory")
            
            if not full_path.exists():
                raise FileNotFoundError(f"Directory not found: {directory}")
            
            if not full_path.is_dir():
                raise ValueError(f"Path is not a directory: {directory}")
            
            files = []
            for item in full_path.iterdir():
                files.append({
                    "name": item.name,
                    "path": str(item.relative_to(self.base_path)),
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else None
                })
            
            logger.info(f"Listed files in: {directory}")
            return files
        
        except Exception as e:
            logger.error(f"Error listing files in {directory}: {str(e)}")
            raise
    
    def delete_file(self, file_path: str) -> str:
        """
        Delete a file
        
        Args:
            file_path: Path to the file (relative to base_path)
            
        Returns:
            Success message
        """
        try:
            full_path = self.base_path / file_path
            # Security: Ensure path is within base_path
            if not str(full_path.resolve()).startswith(str(self.base_path.resolve())):
                raise ValueError("Path outside allowed directory")
            
            if not full_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            full_path.unlink()
            logger.info(f"Deleted file: {file_path}")
            return f"Successfully deleted {file_path}"
        
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {str(e)}")
            raise

