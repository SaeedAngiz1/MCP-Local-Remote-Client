"""
Data Processing Tools for MCP

Provides tools for processing and transforming data.
"""

import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class DataTools:
    """Tools for data processing"""
    
    def process_data(self, data: str, operation: str, **kwargs) -> Any:
        """
        Process and transform data
        
        Args:
            data: Data to process (JSON string)
            operation: Operation to perform (filter, sort, transform, aggregate)
            **kwargs: Additional operation-specific parameters
            
        Returns:
            Processed data
        """
        try:
            # Parse input data
            if isinstance(data, str):
                parsed_data = json.loads(data)
            else:
                parsed_data = data
            
            # Perform operation
            if operation == "filter":
                return self._filter_data(parsed_data, **kwargs)
            elif operation == "sort":
                return self._sort_data(parsed_data, **kwargs)
            elif operation == "transform":
                return self._transform_data(parsed_data, **kwargs)
            elif operation == "aggregate":
                return self._aggregate_data(parsed_data, **kwargs)
            else:
                raise ValueError(f"Unknown operation: {operation}")
        
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON data: {str(e)}")
            raise ValueError(f"Invalid JSON data: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing data: {str(e)}")
            raise
    
    def _filter_data(self, data: Any, condition: str = None, **kwargs) -> Any:
        """Filter data based on condition"""
        if isinstance(data, list):
            # Simple filtering - can be extended
            if condition:
                # In a real implementation, you'd parse and evaluate the condition
                return [item for item in data if self._evaluate_condition(item, condition)]
            return data
        return data
    
    def _sort_data(self, data: Any, key: str = None, reverse: bool = False, **kwargs) -> Any:
        """Sort data"""
        if isinstance(data, list):
            if key:
                return sorted(data, key=lambda x: x.get(key, 0) if isinstance(x, dict) else x, reverse=reverse)
            return sorted(data, reverse=reverse)
        return data
    
    def _transform_data(self, data: Any, mapping: Dict[str, str] = None, **kwargs) -> Any:
        """Transform data structure"""
        if isinstance(data, list) and mapping:
            return [
                {mapping.get(k, k): v for k, v in item.items()}
                if isinstance(item, dict) else item
                for item in data
            ]
        return data
    
    def _aggregate_data(self, data: Any, function: str = "sum", field: str = None, **kwargs) -> Any:
        """Aggregate data"""
        if isinstance(data, list) and field:
            values = [
                item.get(field) if isinstance(item, dict) else item
                for item in data
                if item.get(field) is not None if isinstance(item, dict) else item is not None
            ]
            
            if function == "sum":
                return sum(values) if all(isinstance(v, (int, float)) for v in values) else None
            elif function == "avg":
                return sum(values) / len(values) if values and all(isinstance(v, (int, float)) for v in values) else None
            elif function == "count":
                return len(values)
            elif function == "min":
                return min(values) if values else None
            elif function == "max":
                return max(values) if values else None
        
        return data
    
    def _evaluate_condition(self, item: Any, condition: str) -> bool:
        """Evaluate a condition (simplified implementation)"""
        # This is a simplified implementation
        # In production, you'd want a proper expression evaluator
        try:
            if isinstance(item, dict):
                # Simple key-value check
                if "==" in condition:
                    key, value = condition.split("==", 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    return str(item.get(key, "")) == value
            return True
        except:
            return True

