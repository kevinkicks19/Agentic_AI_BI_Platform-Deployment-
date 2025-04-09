from typing import Dict, Any, List
import logging
from datetime import datetime, timezone
from .base_workflow import BaseWorkflow
from .workflow_registry import workflow_registry
from app.agents.coach_agent import CoachAgent
from app.agents.router_agent import RouterAgent
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProblemDiscoveryWorkflow(BaseWorkflow):
    """A workflow for discovering and analyzing business problems through agent interaction."""
    
    def __init__(self):
        super().__init__(
            workflow_id="problem_discovery",
            name="Problem Discovery Workflow",
            description="A workflow for discovering and analyzing business problems"
        )
        self.max_conversation_turns = 10
        self.coach_agent = CoachAgent()
        self.router_agent = RouterAgent()
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate the input data for the workflow.
        
        Args:
            input_data: Dictionary containing:
                - problem_description: String describing the business problem
                - context: Optional dictionary with any pre-existing context
        
        Returns:
            bool: True if input is valid, False otherwise
        """
        required_fields = ["problem_description"]
        return all(field in input_data for field in required_fields)
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the problem discovery workflow.
        
        Args:
            input_data: Dictionary containing the input parameters
        
        Returns:
            Dict[str, Any]: Results including the inception document
        """
        try:
            # Start the discovery conversation
            conversation_state = {
                "query": input_data["problem_description"],
                "context": input_data.get("context", {})
            }
            
            # Conduct the discovery conversation
            conversation_result = await self.coach_agent.conduct_discovery_conversation(conversation_state)
            
            if not conversation_result.get("summary"):
                raise Exception("Failed to generate problem summary")
            
            # Route to appropriate solution
            routing_result = await self.router_agent.analyze_problem(conversation_result["summary"])
            
            # Create inception document
            inception_doc = {
                "timestamp": datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"),
                "problem_summary": conversation_result["summary"],
                "solution_plan": routing_result,
                "conversation_summary": conversation_result["conversation_history"],
                "metadata": {
                    "workflow_version": "1.0",
                    "agents_used": ["CoachAgent", "RouterAgent"],
                    "conversation_turns": len(conversation_result["conversation_history"]),
                    "topics_covered": conversation_result["topics_covered"],
                    "key_insights": conversation_result["key_insights"]
                }
            }
            
            return {
                "status": "success",
                "inception_document": inception_doc
            }
            
        except Exception as e:
            logger.error(f"Error in ProblemDiscoveryWorkflow: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

# Register the workflow
workflow_registry.register_workflow(ProblemDiscoveryWorkflow) 