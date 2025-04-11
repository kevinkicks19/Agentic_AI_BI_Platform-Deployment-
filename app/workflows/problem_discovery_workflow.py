from typing import Dict, Any, List
import logging
from datetime import datetime
import traceback
from app.workflows.base_workflow import BaseWorkflow
from app.agents.coach_agent import CoachAgent
from app.agents.router_agent import RouterAgent
from app.agents.user_simulation_agent import UserSimulationAgent
from .workflow_registry import workflow_registry

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProblemDiscoveryWorkflow(BaseWorkflow):
    """A workflow for discovering and analyzing business problems through coaching and routing."""
    
    def __init__(self):
        super().__init__(
            workflow_id="problem_discovery",
            name="Problem Discovery Workflow",
            description="A workflow for discovering and analyzing business problems through coaching and routing"
        )
        self.max_conversation_turns = 10
        self.conversation_history = []
        logger.info("ProblemDiscoveryWorkflow initialized")
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate the input data for the workflow.
        
        Args:
            input_data: Dictionary containing:
                - problem_description: Initial description of the problem
                - user_profile: Profile for the user simulation agent
        
        Returns:
            bool: True if input is valid, False otherwise
        """
        required_fields = ["problem_description", "user_profile"]
        is_valid = all(field in input_data for field in required_fields)
        if not is_valid:
            missing_fields = [field for field in required_fields if field not in input_data]
            logger.error(f"Missing required fields: {missing_fields}")
        return is_valid
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the problem discovery workflow
        
        Args:
            input_data: Dictionary containing:
                - problem_description: Initial description of the problem
                - user_profile: Profile for the user simulation agent
                
        Returns:
            Dict containing the workflow results
        """
        try:
            logger.info("Starting workflow execution")
            
            # Validate input
            if not self.validate_input(input_data):
                raise ValueError("Invalid input data")
            
            # Initialize agents
            logger.info("Initializing agents")
            coach_agent = CoachAgent()
            router_agent = RouterAgent()
            user_agent = UserSimulationAgent(input_data["user_profile"])
            
            # Start the discovery conversation
            logger.info("Starting discovery conversation")
            initial_message = f"I'm facing this challenge: {input_data['problem_description']}"
            user_response = user_agent.respond_to_coach(initial_message)
            logger.info(f"Initial user response received: {user_response}")
            
            # Conduct the coaching conversation
            conversation_state = {
                "current_topic": "initial_problem",
                "topics_covered": set(),
                "problem_summary": "",
                "solution_requirements": []
            }
            
            # Conduct the conversation
            logger.info("Starting coaching conversation")
            final_state = self._conduct_conversation(
                coach_agent,
                user_agent,
                conversation_state
            )
            logger.info("Coaching conversation completed")
            
            # Generate problem summary
            logger.info("Generating problem summary")
            problem_summary = coach_agent.prepare_routing_summary()
            
            # Route to appropriate solution
            logger.info("Planning solution")
            solution_plan = router_agent.create_solution_plan(problem_summary)
            
            # Create inception document
            logger.info("Creating inception document")
            inception_doc = {
                "timestamp": datetime.now().isoformat(),
                "problem_summary": problem_summary,
                "solution_plan": solution_plan,
                "conversation_summary": self._summarize_conversation(final_state),
                "metadata": {
                    "workflow_version": "1.0",
                    "agents_used": ["coach", "router", "user"],
                    "topics_covered": list(final_state["topics_covered"]),
                    "conversation_turns": len(self.conversation_history)
                }
            }
            
            logger.info("Workflow completed successfully")
            return {
                "status": "success",
                "inception_document": inception_doc,
                "conversation_history": self.conversation_history
            }
            
        except Exception as e:
            logger.error(f"Error in problem discovery workflow: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc()
            }
    
    def _conduct_conversation(
        self,
        coach_agent: CoachAgent,
        user_agent: UserSimulationAgent,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Conduct the coaching conversation
        
        Args:
            coach_agent: The coaching agent
            user_agent: The user simulation agent
            state: Current conversation state
            
        Returns:
            Updated conversation state
        """
        turn_count = 0
        current_message = "Hello! I'm here to help you explore your challenge. Could you tell me more about what you're facing?"
        
        while turn_count < self.max_conversation_turns:
            # Get user response
            user_response = user_agent.respond_to_coach(current_message)
            self.conversation_history.append({
                "role": "user",
                "content": user_response["content"]
            })
            
            # Get coach's next message
            coach_response = coach_agent.continue_coaching(user_response["content"])
            
            # Update conversation state
            current_topic_index = min(coach_agent.current_topic_index, len(coach_agent.topics_to_cover) - 1)
            state["topics_covered"].add(coach_agent.topics_to_cover[current_topic_index])
            state["problem_summary"] = coach_agent.problem_summary
            
            self.conversation_history.append({
                "role": "coach",
                "content": coach_response
            })
            
            # Check if conversation should continue
            if coach_agent.is_conversation_complete():
                break
            
            current_message = coach_response
            turn_count += 1
        
        return state
    
    def _summarize_conversation(self, state: Dict[str, Any]) -> str:
        """Generate a summary of the conversation"""
        topics_covered = ', '.join(state['topics_covered'])
        requirements = '\n'.join(f"- {req}" for req in state.get('solution_requirements', []))
        problem_summary = state.get('problem_summary', 'No summary available')
        
        return f"""Conversation Summary:
Topics Covered: {topics_covered}
Key Requirements Identified:
{requirements}
Final Problem Understanding: {problem_summary}
"""

# Register the workflow
workflow_registry.register_workflow(ProblemDiscoveryWorkflow) 