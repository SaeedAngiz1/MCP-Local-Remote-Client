"""
Unit tests for MCP server implementation
"""

import pytest
import json
import tempfile
from pathlib import Path
from src.tools.file_tools import FileTools
from src.tools.data_tools import DataTools


class TestFileTools:
    """Tests for FileTools"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.file_tools = FileTools(base_path=self.temp_dir)
    
    def test_write_and_read_file(self):
        """Test writing and reading a file"""
        test_content = "Hello, MCP!"
        test_file = "test.txt"
        
        # Write file
        result = self.file_tools.write_file(test_file, test_content)
        assert "Successfully" in result
        
        # Read file
        content = self.file_tools.read_file(test_file)
        assert content == test_content
    
    def test_list_files(self):
        """Test listing files in directory"""
        # Create test files
        self.file_tools.write_file("file1.txt", "content1")
        self.file_tools.write_file("file2.txt", "content2")
        
        # List files
        files = self.file_tools.list_files(".")
        assert len(files) >= 2
        file_names = [f["name"] for f in files]
        assert "file1.txt" in file_names
        assert "file2.txt" in file_names
    
    def test_read_nonexistent_file(self):
        """Test reading a file that doesn't exist"""
        with pytest.raises(FileNotFoundError):
            self.file_tools.read_file("nonexistent.txt")


class TestDataTools:
    """Tests for DataTools"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.data_tools = DataTools()
    
    def test_sort_data(self):
        """Test sorting data"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        data_json = json.dumps(data)
        
        result = self.data_tools.process_data(data_json, "sort")
        sorted_data = json.loads(result) if isinstance(result, str) else result
        
        assert sorted_data == [1, 1, 2, 3, 4, 5, 6, 9]
    
    def test_aggregate_data(self):
        """Test aggregating data"""
        data = [{"value": 10}, {"value": 20}, {"value": 30}]
        data_json = json.dumps(data)
        
        result = self.data_tools.process_data(
            data_json,
            "aggregate",
            function="sum",
            field="value"
        )
        
        # Result should be a number (sum of values)
        assert result == 60 or (isinstance(result, str) and "60" in result)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

