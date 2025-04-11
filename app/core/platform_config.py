"""
Platform configuration and initialization.
"""
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

# Get logger for this module
logger = logging.getLogger(__name__)

class PlatformConfig:
    """Platform configuration and initialization."""
    
    def __init__(self):
        """Initialize platform configuration."""
        self.config = {}
        self.clients = {}
        self._initialize_mcp()
        self._initialize_mem0()
        self._initialize_phoenix()
        self._initialize_llm()
        logger.info("Platform configuration initialized successfully")
    
    def _initialize_mcp(self):
        """Initialize MCP configuration."""
        try:
            from mem0 import MCPClient
            self.clients["mcp"] = MCPClient()
            logger.info("MCP client initialized successfully")
        except ImportError:
            logger.warning("MCP client not available")
            self.clients["mcp"] = None
    
    def _initialize_mem0(self):
        """Initialize mem0 configuration."""
        try:
            from mem0 import MemoryClient
            api_key = os.getenv("MEM0_API_KEY")
            if not api_key:
                logger.warning("MEM0_API_KEY not found in environment variables")
                self.clients["mem0"] = None
                return
                
            self.clients["mem0"] = MemoryClient(api_key=api_key)
            logger.info("mem0 client initialized successfully")
        except ImportError:
            logger.warning("mem0 client not available")
            self.clients["mem0"] = None
    
    def _initialize_phoenix(self):
        """Initialize Phoenix Arize configuration."""
        try:
            # Check if Phoenix is installed
            import phoenix.server as px_server
            logger.info("Phoenix package found, attempting to initialize...")
            
            # Initialize Phoenix with default configuration
            try:
                self.clients["phoenix"] = px_server
                logger.info("Phoenix Arize client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Phoenix: {str(e)}")
                self.clients["phoenix"] = None
                
        except ImportError as e:
            logger.warning(f"Phoenix package not found: {str(e)}")
            self.clients["phoenix"] = None
        except Exception as e:
            logger.warning(f"Unexpected error initializing Phoenix: {str(e)}")
            self.clients["phoenix"] = None
    
    def _initialize_llm(self):
        """Initialize LLM configuration."""
        self.config["llm"] = {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 1000
        }
        logger.info(f"LLM configuration initialized with provider: {self.config['llm']['provider']}")
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration."""
        return self.config
    
    def get_clients(self) -> Dict[str, Any]:
        """Get current clients."""
        return self.clients
    
    def update_config(self, new_config: Dict[str, Any]):
        """Update the configuration with new values."""
        try:
            # Update LLM configuration if provided
            if "llm" in new_config:
                self.config["llm"].update(new_config["llm"])
                self._initialize_llm()  # Reinitialize LLM with new config
            
            # Update tools configuration if provided
            if "tools" in new_config:
                self.config["tools"].update(new_config["tools"])
            
            logger.info("Configuration updated successfully")
            
        except Exception as e:
            logger.error(f"Failed to update configuration: {str(e)}")
            raise

# Create global platform instance
platform = PlatformConfig() 