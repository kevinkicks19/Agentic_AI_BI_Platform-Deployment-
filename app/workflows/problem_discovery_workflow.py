from typing import Dict, Any, List
import logging
from datetime import datetime
from .base_workflow import BaseWorkflow
from .workflow_registry import workflow_registry
from app.agents.coach_agent import CoachAgent
from app.agents.router_agent import RouterAgent

logger = logging.getLogger(__name__)

class ProblemDiscoveryWorkflow(BaseWorkflow):
    """A workflow for discovering and analyzing business problems through agent interaction."""
    
    def __init__(self, workflow_id: str, name: str, description: str):
        super().__init__(workflow_id, name, description)
        
        # Initialize agents
        self.coach_agent = CoachAgent()
        self.router_agent = RouterAgent()
        
        # Define workflow steps
        self.add_step(
            "initial_conversation",
            "Coach agent conducts initial conversation to understand the problem"
        )
        self.add_step(
            "problem_summary",
            "Coach agent summarizes the gathered information"
        )
        self.add_step(
            "solution_planning",
            "Router agent analyzes problem and creates solution plan"
        )
        self.add_step(
            "inception_document",
            "Generate comprehensive inception document with problem analysis and solution approach"
        )
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate the input data for the workflow.
        
        Args:
            input_data: Dictionary containing:
                - initial_query: String describing the initial business problem
                - user_context: Optional dictionary with any pre-existing context
        
        Returns:
            bool: True if input is valid, False otherwise
        """
        if "initial_query" not in input_data:
            logger.error("Missing initial query in input data")
            return False
        
        if not isinstance(input_data["initial_query"], str) or not input_data["initial_query"].strip():
            logger.error("Initial query must be a non-empty string")
            return False
        
        if "user_context" in input_data and not isinstance(input_data["user_context"], dict):
            logger.error("User context must be a dictionary")
            return False
        
        return True
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the problem discovery workflow.
        
        Args:
            input_data: Dictionary containing the input parameters
        
        Returns:
            Dict[str, Any]: Results including the inception document
        """
        try:
            # Start workflow
            await self.pre_execute()
            
            # Step 1: Initial Conversation
            self.current_step = 0
            await self.update_step_status(self.current_step, "running")
            conversation_results = await self._conduct_conversation(
                input_data["initial_query"],
                input_data.get("user_context", {})
            )
            await self.update_step_status(
                self.current_step, 
                "completed",
                {"conversation_summary": conversation_results["summary"]}
            )
            
            # Step 2: Problem Summary
            self.current_step = 1
            await self.update_step_status(self.current_step, "running")
            problem_summary = await self._generate_problem_summary(conversation_results)
            await self.update_step_status(
                self.current_step,
                "completed",
                {"problem_summary": problem_summary}
            )
            
            # Step 3: Solution Planning
            self.current_step = 2
            await self.update_step_status(self.current_step, "running")
            solution_plan = await self._create_solution_plan(problem_summary)
            await self.update_step_status(
                self.current_step,
                "completed",
                {"solution_plan": solution_plan}
            )
            
            # Step 4: Inception Document
            self.current_step = 3
            await self.update_step_status(self.current_step, "running")
            inception_document = await self._generate_inception_document(
                problem_summary,
                solution_plan
            )
            await self.update_step_status(
                self.current_step,
                "completed",
                {"inception_document": inception_document}
            )
            
            # Complete workflow
            self.results = {
                "problem_summary": problem_summary,
                "solution_plan": solution_plan,
                "inception_document": inception_document,
                "completed_at": datetime.utcnow()
            }
            await self.post_execute()
            
            return self.results
            
        except Exception as e:
            await self.handle_error(e, self.current_step)
            raise
    
    async def _conduct_conversation(
        self,
        initial_query: str,
        user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Have the coach agent conduct a conversation to understand the problem."""
        # Initialize conversation with context
        conversation_state = {
            "query": initial_query,
            "context": user_context,
            "topics_covered": [],
            "questions_asked": [],
            "key_insights": []
        }
        
        # Coach agent leads the conversation
        conversation_results = await self.coach_agent.conduct_discovery_conversation(conversation_state)
        return conversation_results
    
    async def _generate_problem_summary(self, conversation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Have the coach agent generate a structured summary of the problem."""
        return await self.coach_agent.prepare_routing_summary()
    
    async def _create_solution_plan(self, problem_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Have the router agent analyze the problem and create a solution plan."""
        return await self.router_agent.create_solution_plan(problem_summary)
    
    async def _generate_inception_document(
        self,
        problem_summary: Dict[str, Any],
        solution_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate a comprehensive inception document."""
        inception_document = {
            "title": "Project Inception Document",
            "created_at": datetime.utcnow(),
            "sections": {
                "executive_summary": {
                    "problem_statement": problem_summary.get("problem_description", ""),
                    "proposed_solution": solution_plan.get("summary", ""),
                    "expected_outcomes": solution_plan.get("expected_outcomes", [])
                },
                "problem_analysis": {
                    "context": problem_summary.get("context_background", ""),
                    "stakeholders": problem_summary.get("stakeholders", []),
                    "constraints": problem_summary.get("constraints_limitations", []),
                    "success_criteria": problem_summary.get("goals_outcomes", [])
                },
                "solution_approach": {
                    "methodology": solution_plan.get("methodology", ""),
                    "required_agents": solution_plan.get("required_agents", []),
                    "timeline": solution_plan.get("estimated_timeline", {}),
                    "deliverables": solution_plan.get("deliverables", []),
                    "risks_mitigations": solution_plan.get("risks", [])
                },
                "next_steps": {
                    "immediate_actions": solution_plan.get("next_steps", []),
                    "resource_requirements": solution_plan.get("resource_requirements", {}),
                    "success_metrics": solution_plan.get("success_metrics", [])
                }
            },
            "metadata": {
                "workflow_id": self.workflow_id,
                "generated_by": "ProblemDiscoveryWorkflow",
                "version": "1.0"
            }
        }
        return inception_document

# Register the workflow
workflow_registry.register_workflow(ProblemDiscoveryWorkflow) 