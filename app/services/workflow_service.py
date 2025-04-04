from typing import Dict, Any, Optional
from app.agents.agent_factory import AgentFactory
from app.integrations.integration_manager import IntegrationManager
from app.config.settings import settings
import logging
import uuid
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowService:
    def __init__(self):
        self.agent_factory = AgentFactory("config/agents.yaml")
        self.agents = self.agent_factory.create_agents()
        self.current_session = None
        self.conversation_history = []
        self.problem_summary = None
        self.solution_plan = None
        self.integration_manager = IntegrationManager(
            mem0_api_key=settings.MEM0_API_KEY,
            arize_api_key=settings.ARIZE_API_KEY,
            arize_project_name=settings.ARIZE_PROJECT_NAME
        )
    
    async def start_session(self, problem: str) -> Dict[str, Any]:
        """Start a new coaching session"""
        try:
            logger.info("Starting new coaching session")
            self.current_session = str(uuid.uuid4())
            self.conversation_history = []
            self.problem_summary = None
            self.solution_plan = None
            
            # Get the business coach agent
            coach = self.agents.get("Business_Coach")
            if not coach:
                raise ValueError("Business Coach agent not found")
            
            # Add initial problem to history
            self.conversation_history.append({
                "role": "user",
                "content": problem,
                "timestamp": datetime.now().isoformat()
            })
            
            # Get initial response
            response = await coach.process_message(problem, None)
            self.conversation_history.append({
                **response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Store interaction in integrations with enhanced metadata
            self.integration_manager.store_interaction(
                session_id=self.current_session,
                message={
                    "type": "start_session",
                    "problem": problem,
                    "response": response,
                    "agent": "Business_Coach",
                    "timestamp": datetime.now().isoformat(),
                    "metadata": {
                        "session_type": "coaching",
                        "initial_problem": problem,
                        "agent_capabilities": coach.capabilities
                    }
                }
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error starting session: {str(e)}")
            return {
                "status": "error",
                "content": f"Error starting session: {str(e)}",
                "role": "system"
            }
    
    async def continue_session(self, response: str) -> Dict[str, Any]:
        """Continue the current session"""
        try:
            if not self.current_session:
                raise ValueError("No active coaching session")
            
            logger.info("Continuing coaching session")
            
            # Get the business coach agent
            coach = self.agents.get("Business_Coach")
            if not coach:
                raise ValueError("Business Coach agent not found")
            
            # Add user response to history
            self.conversation_history.append({
                "role": "user",
                "content": response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Get coach response
            coach_response = await coach.process_message(response, None)
            self.conversation_history.append({
                **coach_response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Check if we have enough exchanges to confirm problem summary
            if len(self.conversation_history) >= 4:
                self.problem_summary = self._extract_problem_summary()
            
            # Store interaction in integrations with enhanced metadata
            self.integration_manager.store_interaction(
                session_id=self.current_session,
                message={
                    "type": "continue_session",
                    "response": response,
                    "agent_response": coach_response,
                    "agent": "Business_Coach",
                    "timestamp": datetime.now().isoformat(),
                    "metadata": {
                        "conversation_length": len(self.conversation_history),
                        "has_problem_summary": self.problem_summary is not None,
                        "agent_capabilities": coach.capabilities
                    }
                }
            )
            
            return coach_response
            
        except ValueError as e:
            logger.error(f"Value error in continue_session: {str(e)}")
            return {
                "status": "error",
                "content": str(e),
                "role": "system"
            }
        except Exception as e:
            logger.error(f"Error in continue_session: {str(e)}")
            return {
                "status": "error",
                "content": f"Error continuing session: {str(e)}",
                "role": "system"
            }
    
    def _extract_problem_summary(self) -> Dict[str, Any]:
        """Extract problem summary from conversation history"""
        # Implementation for extracting problem summary
        return {
            "problem": "Extracted problem summary",
            "key_points": ["Point 1", "Point 2"],
            "context": "Problem context"
        }
    
    async def confirm_problem_summary(self) -> Dict[str, Any]:
        """Confirm the problem summary and generate solution plan"""
        try:
            if not self.problem_summary:
                raise ValueError("No problem summary available")
            
            logger.info("Confirming problem summary")
            
            # Get the router agent
            router = self.agents.get("Problem_Router")
            if not router:
                raise ValueError("Problem Router agent not found")
            
            # Generate solution plan
            plan = await router.create_solution_plan(self.problem_summary)
            self.solution_plan = plan
            
            # Store interaction in integrations with enhanced metadata
            self.integration_manager.store_interaction(
                session_id=self.current_session,
                message={
                    "type": "confirm_summary",
                    "summary": self.problem_summary,
                    "plan": plan,
                    "agent": "Problem_Router",
                    "timestamp": datetime.now().isoformat(),
                    "metadata": {
                        "conversation_length": len(self.conversation_history),
                        "plan_complexity": len(plan.get("solution_plan", {}).get("steps", [])),
                        "agent_capabilities": router.capabilities
                    }
                }
            )
            
            return {
                "status": "success",
                "summary": self.problem_summary,
                "plan": plan
            }
            
        except ValueError as e:
            logger.error(f"Value error in confirm_summary: {str(e)}")
            return {
                "status": "error",
                "content": str(e),
                "role": "system"
            }
        except Exception as e:
            logger.error(f"Error in confirm_summary: {str(e)}")
            return {
                "status": "error",
                "content": f"Error confirming summary: {str(e)}",
                "role": "system"
            }
    
    def get_session_status(self) -> Dict[str, Any]:
        """Get current session status"""
        # Get integration context
        integration_context = {}
        if self.current_session:
            integration_context = self.integration_manager.get_session_context(self.current_session)
        
        return {
            "status": "active" if self.current_session else "inactive",
            "has_problem_summary": self.problem_summary is not None,
            "has_solution_plan": self.solution_plan is not None,
            "session_id": self.current_session,
            "conversation_history": self.conversation_history,
            "integration_context": integration_context
        }
    
    def analyze_session(self) -> Dict[str, Any]:
        """Analyze the current session's performance and context"""
        if not self.current_session:
            return {"error": "No active session"}
        
        session_id = self.current_session
        return self.integration_manager.analyze_session(session_id)
    
    def clear_session(self) -> None:
        """Clear the current session"""
        if self.current_session:
            session_id = self.current_session
            self.integration_manager.clear_session(session_id)
            self.current_session = None
            self.conversation_history = []
            self.problem_summary = None
            self.solution_plan = None 