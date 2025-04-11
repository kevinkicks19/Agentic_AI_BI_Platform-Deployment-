"""
Basic test script for mem0ai integration.
"""
import os
from dotenv import load_dotenv
import uuid
import json

# Load environment variables
load_dotenv()

def test_basic():
    """Test basic mem0ai functionality."""
    print("\n=== Testing Basic mem0ai Functionality ===")
    
    try:
        # Import mem0ai
        from mem0 import MemoryClient, __version__
        print(f"✓ Successfully imported mem0 version {__version__}")
        
        # Get API key and IDs
        api_key = os.getenv("MEM0_API_KEY")
        org_id = os.getenv("MEM0_ORG_ID")
        project_id = os.getenv("MEM0_PROJECT_ID")
        
        if not all([api_key, org_id, project_id]):
            print("✗ Missing required environment variables:")
            print(f"  API Key: {'✓' if api_key else '✗'}")
            print(f"  Org ID: {'✓' if org_id else '✗'}")
            print(f"  Project ID: {'✓' if project_id else '✗'}")
            return
            
        print("✓ Found all required credentials")
        print(f"API Key: {api_key[:8]}...")
        print(f"Org ID: {org_id}")
        print(f"Project ID: {project_id}")
        
        # Initialize client
        client = MemoryClient(
            api_key=api_key,
            org_id=org_id,
            project_id=project_id
        )
        print("✓ Successfully initialized MemoryClient")
        
        # Test basic functionality
        print("\nTesting basic functionality...")
        
        # Generate test IDs
        agent_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())
        
        # Create a test memory with minimal parameters
        memory_data = {
            "messages": [{
                "role": "user",
                "content": "Test message"
            }],
            "agent_id": agent_id,
            "user_id": user_id,
            "output_format": "v1.1"
        }
        
        print("\nCreating memory with data:")
        print(json.dumps(memory_data, indent=2))
        
        try:
            memory_response = client.add(**memory_data)
            print("\nMemory Creation Response:")
            print(json.dumps(memory_response, indent=2))
        except Exception as e:
            print(f"\n✗ Memory creation error: {str(e)}")
            print("\nTrying alternative format...")
            
            # Try alternative format
            memory_response = client.add(
                messages=[{
                    "role": "user",
                    "content": "Test message"
                }],
                agent_id=agent_id,
                user_id=user_id,
                output_format="v1.1"
            )
            print("\nAlternative Memory Creation Response:")
            print(json.dumps(memory_response, indent=2))
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")

if __name__ == "__main__":
    test_basic() 