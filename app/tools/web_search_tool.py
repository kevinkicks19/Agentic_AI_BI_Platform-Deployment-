from typing import Dict, Any
import logging
import aiohttp
from app.tools.base_tool import BaseTool

logger = logging.getLogger(__name__)

class WebSearchTool(BaseTool):
    """Tool for performing web searches."""
    
    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for information"
        )
        self.parameters = {
            "query": {
                "type": "string",
                "description": "The search query",
                "required": True
            },
            "num_results": {
                "type": "integer",
                "description": "Number of results to return",
                "required": False,
                "default": 5
            }
        }
        self.api_key = None  # Would be loaded from environment variables
        self.search_url = "https://api.search.example.com/v1/search"  # Example URL
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the web search."""
        if not self.validate_parameters(**kwargs):
            return {
                "status": "error",
                "error": "Invalid parameters"
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    "q": kwargs["query"],
                    "limit": kwargs.get("num_results", 5),
                    "api_key": self.api_key
                }
                
                async with session.get(self.search_url, params=params) as response:
                    if response.status == 200:
                        results = await response.json()
                        return {
                            "status": "success",
                            "results": results
                        }
                    else:
                        return {
                            "status": "error",
                            "error": f"API returned status {response.status}"
                        }
        
        except Exception as e:
            logger.error(f"Error performing web search: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            } 