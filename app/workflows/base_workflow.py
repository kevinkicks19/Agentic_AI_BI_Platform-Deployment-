from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseWorkflow(ABC):
    """Base class for all workflows in the platform."""
    
    def __init__(self, workflow_id: str, name: str, description: str):
        """Initialize the workflow with basic metadata.
        
        Args:
            workflow_id: Unique identifier for the workflow
            name: Human-readable name of the workflow
            description: Detailed description of what the workflow does
        """
        self.workflow_id = workflow_id
        self.name = name
        self.description = description
        self.created_at = datetime.utcnow()
        self.status = "initialized"
        self.steps: List[Dict[str, Any]] = []
        self.current_step = 0
        self.metadata: Dict[str, Any] = {}
        self.results: Dict[str, Any] = {}
        
    @abstractmethod
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate the input data before starting the workflow.
        
        Args:
            input_data: Dictionary containing the input parameters
            
        Returns:
            bool: True if input is valid, False otherwise
        """
        pass
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the workflow with the given input data.
        
        Args:
            input_data: Dictionary containing the input parameters
            
        Returns:
            Dict[str, Any]: Results of the workflow execution
        """
        pass
    
    async def pre_execute(self) -> None:
        """Perform any necessary setup before workflow execution."""
        self.status = "running"
        logger.info(f"Starting workflow: {self.name} ({self.workflow_id})")
    
    async def post_execute(self) -> None:
        """Perform any necessary cleanup after workflow execution."""
        self.status = "completed"
        logger.info(f"Completed workflow: {self.name} ({self.workflow_id})")
    
    def add_step(self, step_name: str, description: str) -> None:
        """Add a step to the workflow.
        
        Args:
            step_name: Name of the step
            description: Description of what the step does
        """
        step = {
            "step_id": len(self.steps) + 1,
            "name": step_name,
            "description": description,
            "status": "pending",
            "started_at": None,
            "completed_at": None,
            "results": None
        }
        self.steps.append(step)
    
    async def update_step_status(self, step_id: int, status: str, results: Optional[Dict[str, Any]] = None) -> None:
        """Update the status and results of a workflow step.
        
        Args:
            step_id: ID of the step to update
            status: New status of the step
            results: Optional results from the step execution
        """
        if 0 <= step_id < len(self.steps):
            self.steps[step_id]["status"] = status
            if status == "running":
                self.steps[step_id]["started_at"] = datetime.utcnow()
            elif status in ["completed", "failed"]:
                self.steps[step_id]["completed_at"] = datetime.utcnow()
            if results:
                self.steps[step_id]["results"] = results
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the workflow.
        
        Returns:
            Dict[str, Any]: Current status and progress of the workflow
        """
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "status": self.status,
            "current_step": self.current_step,
            "total_steps": len(self.steps),
            "steps": self.steps,
            "created_at": self.created_at,
            "metadata": self.metadata,
            "results": self.results
        }
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the workflow.
        
        Args:
            key: Metadata key
            value: Metadata value
        """
        self.metadata[key] = value
    
    async def handle_error(self, error: Exception, step_id: Optional[int] = None) -> None:
        """Handle workflow errors.
        
        Args:
            error: The exception that occurred
            step_id: Optional ID of the step where the error occurred
        """
        self.status = "failed"
        error_info = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "timestamp": datetime.utcnow()
        }
        
        if step_id is not None:
            await self.update_step_status(step_id, "failed", {"error": error_info})
        
        logger.error(f"Workflow error in {self.name} ({self.workflow_id}): {str(error)}")
        self.results["error"] = error_info 