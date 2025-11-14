"""
API Integration Tools for MCP

Provides tools for making HTTP API calls.
"""

import json
import logging
from typing import Any, Dict, Optional
import httpx

logger = logging.getLogger(__name__)


class APITools:
    """Tools for API integration"""
    
    def __init__(self, timeout: int = 30):
        """
        Initialize API tools
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def call_api(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        body: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP API call
        
        Args:
            url: API endpoint URL
            method: HTTP method (GET, POST, PUT, DELETE)
            headers: HTTP headers
            body: Request body (will be JSON encoded)
            
        Returns:
            Response dictionary with status, headers, and data
        """
        try:
            # Prepare headers
            request_headers = headers or {}
            if "Content-Type" not in request_headers and body:
                request_headers["Content-Type"] = "application/json"
            
            # Prepare request
            request_kwargs = {
                "headers": request_headers,
                "timeout": self.timeout
            }
            
            if body:
                if isinstance(body, str):
                    request_kwargs["content"] = body
                else:
                    request_kwargs["json"] = body
            
            # Make request
            method_upper = method.upper()
            response = await self.client.request(
                method_upper,
                url,
                **request_kwargs
            )
            
            # Parse response
            try:
                response_data = response.json()
            except:
                response_data = response.text
            
            result = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "data": response_data
            }
            
            logger.info(f"API call: {method} {url} - Status: {response.status_code}")
            return result
        
        except httpx.TimeoutException:
            logger.error(f"API call timeout: {url}")
            raise Exception(f"Request to {url} timed out")
        except httpx.RequestError as e:
            logger.error(f"API request error: {str(e)}")
            raise Exception(f"Request failed: {str(e)}")
        except Exception as e:
            logger.error(f"Error making API call: {str(e)}")
            raise
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

