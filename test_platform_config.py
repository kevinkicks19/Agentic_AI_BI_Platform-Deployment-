"""
Test script for platform configuration.
"""
import logging
import traceback
import sys
from logging.handlers import RotatingFileHandler

# Configure logging to write to file
log_handler = RotatingFileHandler('platform_test.log', maxBytes=1024*1024, backupCount=5)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(log_handler)
logging.getLogger().setLevel(logging.INFO)

# Remove any existing stream handlers to keep console output clean
for handler in logging.getLogger().handlers[:]:
    if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
        logging.getLogger().removeHandler(handler)

def print_section(title):
    """Print a section header."""
    print("\n" + "="*50)
    print(title)
    print("="*50)

def test_platform_config():
    """Test platform configuration initialization."""
    print_section("PLATFORM CONFIGURATION TEST")
    
    try:
        from app.core.platform_config import platform
        print("✓ Successfully imported platform configuration")
        
        print("\nClient Status:")
        print("-" * 20)
        # Test MCP client
        mcp_client = platform.get_clients().get("mcp")
        print(f"MCP Client: {'✓ Available' if mcp_client else '✗ Not Available'}")
        
        # Test mem0 client
        mem0_client = platform.get_clients().get("mem0")
        print(f"mem0 Client: {'✓ Available' if mem0_client else '✗ Not Available'}")
        
        # Test Phoenix client
        phoenix_client = platform.get_clients().get("phoenix")
        print(f"Phoenix Client: {'✓ Available' if phoenix_client else '✗ Not Available'}")
        
        print("\nLLM Configuration:")
        print("-" * 20)
        llm_config = platform.get_config().get("llm", {})
        for key, value in llm_config.items():
            print(f"  {key}: {value}")
        
        print("\nPhoenix Details:")
        print("-" * 20)
        try:
            import phoenix.server as px_server
            print("✓ Successfully imported phoenix.server package")
            version = getattr(px_server, '__version__', 'unknown')
            print(f"Phoenix server version: {version}")
        except ImportError as e:
            print(f"✗ Phoenix import error: {str(e)}")
        except Exception as e:
            print(f"✗ Unexpected error: {str(e)}")
            print("Stack trace:")
            print(traceback.format_exc())
            
    except Exception as e:
        print(f"\n✗ Error in test_platform_config: {str(e)}")
        print("Stack trace:")
        print(traceback.format_exc())

if __name__ == "__main__":
    test_platform_config()
    print("\nTest completed.") 