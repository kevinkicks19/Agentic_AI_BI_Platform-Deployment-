"""
Test script for mem0 integration.
"""
import logging
import traceback
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure basic logging
logging.basicConfig(level=logging.INFO)

def print_section(title):
    """Print a section header."""
    print("\n" + "="*50)
    print(title)
    print("="*50)

def test_mem0_integration():
    """Test mem0 integration."""
    print_section("MEM0 INTEGRATION TEST")
    
    try:
        # Test mem0 package availability
        try:
            from mem0 import MemoryClient
            print("✓ mem0 package is available")
            
            # Check for API key
            api_key = os.getenv("MEM0_API_KEY")
            if not api_key:
                print("✗ MEM0_API_KEY not found in environment variables")
                return
            print("✓ MEM0_API_KEY found in environment variables")
            
        except ImportError:
            print("✗ mem0 package is not available")
            print("Please install mem0 package to enable integration")
            return

        # Test platform configuration
        from app.core.platform_config import platform
        print("\nPlatform Configuration:")
        print("-" * 20)
        mem0_client = platform.get_clients().get("mem0")
        print(f"mem0 Client: {'✓ Available' if mem0_client else '✗ Not Available'}")
        
        if not mem0_client:
            print("\n✗ mem0 client not initialized in platform configuration")
            return

        # Test basic mem0 functionality
        print("\nTesting Basic Functionality:")
        print("-" * 20)
        try:
            # Test memory creation
            test_message = {
                "role": "user",
                "content": "Test memory content"
            }
            memory_id = mem0_client.add(
                messages=[test_message],
                metadata={"test": True}
            )
            print("✓ Memory creation successful")
            print(f"Memory ID: {memory_id}")
            
            # Test memory retrieval
            retrieved_memory = mem0_client.get(memory_id)
            print("✓ Memory retrieval successful")
            print(f"Retrieved content: {retrieved_memory['messages'][0]['content']}")
            
            # Test memory search
            search_results = mem0_client.search("test")
            print("✓ Memory search successful")
            print(f"Found {len(search_results)} matching memories")
            
            # Clean up test memory
            mem0_client.delete(memory_id)
            print("✓ Test memory cleanup successful")
            
        except Exception as e:
            print(f"✗ Error testing mem0 functionality: {str(e)}")
            print("Stack trace:")
            print(traceback.format_exc())
            
    except Exception as e:
        print(f"\n✗ Error in test_mem0_integration: {str(e)}")
        print("Stack trace:")
        print(traceback.format_exc())

if __name__ == "__main__":
    test_mem0_integration()
    print("\nTest completed.") 