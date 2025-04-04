from typing import Dict, Optional
import logging
from .mem0_integration import Mem0Integration
from .phoenix_arize_integration import PhoenixArizeIntegration

class IntegrationManager:
    def __init__(self, 
                 mem0_api_key: Optional[str] = None,
                 arize_api_key: Optional[str] = None,
                 arize_project_name: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.mem0 = Mem0Integration(api_key=mem0_api_key)
        self.phoenix_arize = PhoenixArizeIntegration(
            api_key=arize_api_key,
            project_name=arize_project_name
        )

    def store_interaction(self, session_id: str, message: Dict) -> None:
        """Store an interaction in both Mem0 and Phoenix Arize."""
        try:
            # Store in Mem0 for context tracking
            self.mem0.store_interaction(session_id, message)
            
            # Log prediction in Phoenix Arize
            self.phoenix_arize.log_prediction(
                model_name="workflow_agent",
                prediction=message,
                metadata={"session_id": session_id}
            )
            
            self.logger.info(f"Successfully stored interaction for session {session_id}")
        except Exception as e:
            self.logger.error(f"Error storing interaction: {str(e)}")

    def get_session_context(self, session_id: str) -> Dict:
        """Get context and metrics for a session."""
        try:
            mem0_context = self.mem0.retrieve_context(session_id)
            metrics = self.phoenix_arize.get_model_metrics("workflow_agent")
            
            return {
                "session_id": session_id,
                "context": mem0_context,
                "metrics": metrics
            }
        except Exception as e:
            self.logger.error(f"Error getting session context: {str(e)}")
            return {"error": str(e)}

    def analyze_session(self, session_id: str) -> Dict:
        """Analyze session performance and context."""
        try:
            mem0_summary = self.mem0.get_session_summary(session_id)
            performance = self.phoenix_arize.analyze_model_performance("workflow_agent")
            
            return {
                "session_id": session_id,
                "summary": mem0_summary,
                "performance": performance
            }
        except Exception as e:
            self.logger.error(f"Error analyzing session: {str(e)}")
            return {"error": str(e)}

    def clear_session(self, session_id: str) -> None:
        """Clear session data from both integrations."""
        try:
            self.mem0.clear_session(session_id)
            # Note: Phoenix Arize doesn't have a clear method, so we just log
            self.logger.info(f"Cleared session {session_id}")
        except Exception as e:
            self.logger.error(f"Error clearing session: {str(e)}") 