"""
LM Studio Integration Tools for MCP

Provides tools for interacting with LM Studio local LLM server.
"""

import httpx
import logging
from typing import Dict, Any, Optional
import os

logger = logging.getLogger(__name__)


class LMStudioTools:
    """Tools for interacting with LM Studio"""
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize LM Studio tools
        
        Args:
            base_url: Base URL of LM Studio server
                     Defaults to localhost:1234 or from config
        """
        if base_url is None:
            # Try to get from environment or use default
            base_url = os.getenv(
                "LM_STUDIO_URL",
                "http://localhost:1234"
            )
        
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=60.0)
        logger.info(f"LM Studio Tools initialized with URL: {base_url}")
    
    async def generate_text(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 100,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate text using LM Studio
        
        Args:
            prompt: Input prompt
            model: Model name (optional, uses default if not specified)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text response
        """
        try:
            # Get available models if no model specified
            if not model:
                models_response = await self.client.get(f"{self.base_url}/v1/models")
                models_data = models_response.json()
                if models_data.get("data") and len(models_data["data"]) > 0:
                    model = models_data["data"][0]["id"]
                    logger.info(f"Using default model: {model}")
                else:
                    raise Exception("No models available in LM Studio")
            
            # Generate completion
            response = await self.client.post(
                f"{self.base_url}/v1/completions",
                json={
                    "model": model,
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
            )
            
            response.raise_for_status()
            result = response.json()
            
            generated_text = result.get("choices", [{}])[0].get("text", "")
            
            return {
                "text": generated_text,
                "model": model,
                "usage": result.get("usage", {}),
                "finish_reason": result.get("choices", [{}])[0].get("finish_reason", "")
            }
        
        except httpx.ConnectError:
            error_msg = (
                f"Cannot connect to LM Studio at {self.base_url}. "
                "Make sure LM Studio is running with the local server enabled."
            )
            logger.error(error_msg)
            raise Exception(error_msg)
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from LM Studio: {e.response.status_code} - {e.response.text}")
            raise Exception(f"LM Studio API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise
    
    async def chat_completion(
        self,
        messages: list,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Dict[str, Any]:
        """
        Generate chat completion using LM Studio
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model name (optional)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Chat completion response
        """
        try:
            # Get available models if no model specified
            if not model:
                models_response = await self.client.get(f"{self.base_url}/v1/models")
                models_data = models_response.json()
                if models_data.get("data") and len(models_data["data"]) > 0:
                    model = models_data["data"][0]["id"]
                else:
                    raise Exception("No models available in LM Studio")
            
            response = await self.client.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            )
            
            response.raise_for_status()
            result = response.json()
            
            return {
                "message": result.get("choices", [{}])[0].get("message", {}),
                "model": model,
                "usage": result.get("usage", {}),
                "finish_reason": result.get("choices", [{}])[0].get("finish_reason", "")
            }
        
        except httpx.ConnectError:
            error_msg = (
                f"Cannot connect to LM Studio at {self.base_url}. "
                "Make sure LM Studio is running with the local server enabled."
            )
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            logger.error(f"Error in chat completion: {str(e)}")
            raise
    
    async def list_models(self) -> list:
        """
        List available models in LM Studio
        
        Returns:
            List of available models
        """
        try:
            response = await self.client.get(f"{self.base_url}/v1/models")
            response.raise_for_status()
            models_data = response.json()
            return models_data.get("data", [])
        except httpx.ConnectError:
            logger.error(f"Cannot connect to LM Studio at {self.base_url}")
            raise Exception(f"Cannot connect to LM Studio. Make sure it's running.")
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
            raise
    
    async def test_connection(self) -> Dict[str, Any]:
        """
        Test connection to LM Studio
        
        Returns:
            Connection status and available models
        """
        try:
            models = await self.list_models()
            return {
                "status": "connected",
                "url": self.base_url,
                "models_count": len(models),
                "models": [m.get("id", "unknown") for m in models]
            }
        except Exception as e:
            return {
                "status": "disconnected",
                "url": self.base_url,
                "error": str(e)
            }
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

