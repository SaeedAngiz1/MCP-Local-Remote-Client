"""
Test script for LM Studio integration

Run this to verify LM Studio is running and accessible.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.tools.lm_studio_tools import LMStudioTools


async def test_lm_studio():
    """Test LM Studio connection and functionality"""
    
    print("=" * 50)
    print("LM Studio Connection Test")
    print("=" * 50)
    print()
    
    # Initialize tools
    tools = LMStudioTools()
    print(f"Connecting to LM Studio at: {tools.base_url}")
    print()
    
    try:
        # Test 1: Test connection
        print("1. Testing connection...")
        status = await tools.test_connection()
        print(f"   Status: {status['status']}")
        if status['status'] == 'connected':
            print(f"   Models available: {status['models_count']}")
            print(f"   Model names: {status.get('models', [])}")
        else:
            print(f"   Error: {status.get('error', 'Unknown error')}")
            print("\n❌ Cannot connect to LM Studio!")
            print("   Make sure:")
            print("   - LM Studio is running")
            print("   - Local server is enabled (Settings → Local Server)")
            print("   - Server is started on port 1234")
            print("   - CORS is enabled")
            await tools.close()
            return
        print()
        
        # Test 2: List models
        print("2. Listing available models...")
        models = await tools.list_models()
        if models:
            for i, model in enumerate(models, 1):
                model_id = model.get("id", "unknown")
                print(f"   {i}. {model_id}")
        else:
            print("   No models available")
        print()
        
        # Test 3: Generate text
        if status['status'] == 'connected' and models:
            print("3. Testing text generation...")
            test_prompt = "Hello, world! Say something interesting:"
            print(f"   Prompt: {test_prompt}")
            
            try:
                result = await tools.generate_text(
                    prompt=test_prompt,
                    max_tokens=50,
                    temperature=0.7
                )
                print(f"   Generated: {result['text']}")
                print(f"   Model used: {result['model']}")
                print(f"   Tokens used: {result.get('usage', {}).get('total_tokens', 'N/A')}")
                print("\n✅ LM Studio is working correctly!")
            except Exception as e:
                print(f"   ❌ Error generating text: {str(e)}")
        print()
        
        # Test 4: Chat completion
        if status['status'] == 'connected' and models:
            print("4. Testing chat completion...")
            messages = [
                {"role": "user", "content": "What is Python?"}
            ]
            print(f"   Message: {messages[0]['content']}")
            
            try:
                result = await tools.chat_completion(
                    messages=messages,
                    max_tokens=100,
                    temperature=0.7
                )
                message = result.get("message", {})
                content = message.get("content", "")
                print(f"   Response: {content[:200]}...")  # First 200 chars
                print(f"   Model used: {result.get('model', 'N/A')}")
                print("\n✅ Chat completion is working!")
            except Exception as e:
                print(f"   ❌ Error in chat completion: {str(e)}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure LM Studio is running with the local server enabled!")
    
    finally:
        await tools.close()
    
    print()
    print("=" * 50)
    print("Test completed!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(test_lm_studio())

