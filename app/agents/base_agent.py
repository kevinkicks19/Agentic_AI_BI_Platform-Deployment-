from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import os
import json
from app.core.platform_config import PlatformConfig
from litellm import completion
from dotenv import load_dotenv

# Get logger for this module
logger = logging.getLogger(__name__)

load_dotenv()

class BaseAgent:
    def __init__(self, name: str, system_message: str):
        logger.info(f"Initializing {name} agent")
        self.name = name
        self.system_message = system_message
        
        # Initialize platform configuration
        self.platform_config = PlatformConfig()
        self.llm_config = self.platform_config.get_config()["llm"]
        
        # Initialize LiteLLM
        self.model = self.llm_config.get("model", "gpt-3.5-turbo")
        self.api_key = os.getenv("OPENAI_API_KEY")  # You can change this to any provider's API key
        
        # Initialize tools
        self.tools = {}
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize tools for this agent."""
        # Get available tools from registry
        from app.tools.tool_registry import tool_registry
        available_tools = tool_registry.list_tools()
        
        # Add tools to agent's tool set
        for tool_name, tool_schema in available_tools.items():
            tool = tool_registry.get_tool(tool_name)
            if tool:
                self.tools[tool_name] = tool
                logger.info(f"Added tool {tool_name} to agent {self.name}")
    
    def use_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Use a tool by name with the given parameters."""
        if tool_name not in self.tools:
            logger.error(f"Tool {tool_name} not available for agent {self.name}")
            return {
                "status": "error",
                "error": f"Tool {tool_name} not available"
            }
        
        tool = self.tools[tool_name]
        logger.info(f"Agent {self.name} using tool {tool_name}")
        return tool.execute(**kwargs)
    
    def get_available_tools(self) -> Dict[str, Dict[str, Any]]:
        """Get information about available tools."""
        return {
            name: tool.get_schema()
            for name, tool in self.tools.items()
        }
    
    def _log_conversation(self, message: str, response: Dict[str, Any], is_error: bool = False):
        """Log conversation using the central logging system."""
        logger.info(f"\n=== Conversation Log for {self.name} ===")
        logger.info(f"Timestamp: {datetime.now().isoformat()}")
        logger.info("=== System Message ===")
        logger.info(self.system_message)
        logger.info("=== Input Message ===")
        logger.info(message)
        logger.info("=== Response ===")
        logger.info(response['content'])
        logger.info("=== Metadata ===")
        logger.info(response['metadata'])
        
        if is_error:
            logger.error("=== Error Details ===")
            logger.error(response.get('error', 'Unknown error'))
    
    def process_message(self, message: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Process a message using LiteLLM."""
        try:
            messages = [
                {"role": "system", "content": self.system_message}
            ]
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({"role": "user", "content": message})
            
            response = completion(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            result = {
                "content": response.choices[0].message.content,
                "metadata": {
                    "model": self.model,
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
            }
            
            # Log the conversation
            self._log_conversation(message, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            error_response = {
                "content": f"Error: {str(e)}",
                "metadata": {"error": str(e)}
            }
            self._log_conversation(message, error_response, is_error=True)
            return error_response 