from typing import Dict, Type, Optional
import logging
from .base_workflow import BaseWorkflow

logger = logging.getLogger(__name__)

class WorkflowRegistry:
    """Registry for managing and tracking available workflows."""
    
    def __init__(self):
        """Initialize the workflow registry."""
        self._workflows: Dict[str, Type[BaseWorkflow]] = {}
    
    def register_workflow(self, workflow_class: Type[BaseWorkflow]) -> None:
        """Register a new workflow class.
        
        Args:
            workflow_class: The workflow class to register
        """
        workflow_id = workflow_class.__name__.lower()
        if workflow_id in self._workflows:
            logger.warning(f"Workflow {workflow_id} already registered. Overwriting...")
        self._workflows[workflow_id] = workflow_class
        logger.info(f"Registered workflow: {workflow_id}")
    
    def get_workflow_class(self, workflow_id: str) -> Optional[Type[BaseWorkflow]]:
        """Get a workflow class by its ID.
        
        Args:
            workflow_id: ID of the workflow to retrieve
            
        Returns:
            Optional[Type[BaseWorkflow]]: The workflow class if found, None otherwise
        """
        return self._workflows.get(workflow_id.lower())
    
    def create_workflow(self, workflow_id: str, name: str, description: str) -> Optional[BaseWorkflow]:
        """Create a new instance of a workflow.
        
        Args:
            workflow_id: ID of the workflow to create
            name: Name for the workflow instance
            description: Description for the workflow instance
            
        Returns:
            Optional[BaseWorkflow]: New workflow instance if successful, None if workflow not found
        """
        workflow_class = self.get_workflow_class(workflow_id)
        if workflow_class:
            return workflow_class(workflow_id, name, description)
        logger.error(f"Workflow {workflow_id} not found in registry")
        return None
    
    def list_workflows(self) -> Dict[str, Dict]:
        """List all registered workflows with their metadata.
        
        Returns:
            Dict[str, Dict]: Dictionary of workflow IDs and their metadata
        """
        return {
            workflow_id: {
                "name": workflow_class.__name__,
                "description": workflow_class.__doc__ or "No description available",
                "class": workflow_class
            }
            for workflow_id, workflow_class in self._workflows.items()
        }
    
    def unregister_workflow(self, workflow_id: str) -> bool:
        """Unregister a workflow from the registry.
        
        Args:
            workflow_id: ID of the workflow to unregister
            
        Returns:
            bool: True if workflow was unregistered, False if not found
        """
        if workflow_id.lower() in self._workflows:
            del self._workflows[workflow_id.lower()]
            logger.info(f"Unregistered workflow: {workflow_id}")
            return True
        return False

# Create a global workflow registry instance
workflow_registry = WorkflowRegistry() 