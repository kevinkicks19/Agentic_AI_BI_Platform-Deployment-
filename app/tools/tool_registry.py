from typing import Dict, Any, Optional
import logging
from app.tools.base_tool import BaseTool

logger = logging.getLogger(__name__)

class ToolRegistry:
    """Registry for managing available tools."""
    
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        logger.info("Initialized tool registry")
    
    def register_tool(self, tool: BaseTool) -> None:
        """Register a new tool."""
        if tool.name in self.tools:
            logger.warning(f"Tool {tool.name} already registered, overwriting")
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self.tools.get(name)
    
    def list_tools(self) -> Dict[str, Dict[str, Any]]:
        """List all available tools and their schemas."""
        return {
            name: tool.get_schema()
            for name, tool in self.tools.items()
        }
    
    def unregister_tool(self, name: str) -> None:
        """Unregister a tool."""
        if name in self.tools:
            del self.tools[name]
            logger.info(f"Unregistered tool: {name}")
        else:
            logger.warning(f"Tool {name} not found in registry")

# Create a global registry instance
tool_registry = ToolRegistry() 