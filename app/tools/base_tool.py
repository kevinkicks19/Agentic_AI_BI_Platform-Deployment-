from typing import Dict, Any, Optional
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class BaseTool(ABC):
    """Base class for all tools that can be used by agents."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.parameters = {}
        logger.info(f"Initialized tool: {name}")
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool with the given parameters."""
        pass
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the tool's schema including parameters and descriptions."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }
    
    def validate_parameters(self, **kwargs) -> bool:
        """Validate the provided parameters against the tool's schema."""
        required_params = set(self.parameters.keys())
        provided_params = set(kwargs.keys())
        
        if not required_params.issubset(provided_params):
            missing = required_params - provided_params
            logger.error(f"Missing required parameters: {missing}")
            return False
        
        return True 