from typing import Dict, Any
import logging
from mem0 import MemoryClient

logger = logging.getLogger(__name__)

class Mem0Integration:
    def __init__(self, api_key: str):
        """Initialize Mem0 integration with API key"""
        try:
            self.client = MemoryClient(api_key=api_key)
            logger.info("Successfully initialized Mem0 client")
        except Exception as e:
            logger.error(f"Error initializing Mem0 client: {str(e)}")
            raise
    
    def store_interaction(self, session_id: str, message: Dict[str, Any]) -> None:
        """Store an interaction in Mem0"""
        try:
            # Store the interaction with session context
            self.client.store(
                key=f"session_{session_id}",
                value=message,
                metadata={
                    "session_id": session_id,
                    "timestamp": message.get("timestamp"),
                    "type": message.get("type")
                }
            )
            logger.info(f"Successfully stored interaction for session {session_id}")
        except Exception as e:
            logger.error(f"Error storing interaction in Mem0: {str(e)}")
            raise
    
    def retrieve_context(self, session_id: str) -> Dict[str, Any]:
        """Retrieve context for a session"""
        try:
            # Get all interactions for the session
            interactions = self.client.get(
                key=f"session_{session_id}",
                include_metadata=True
            )
            return interactions or {}
        except Exception as e:
            logger.error(f"Error retrieving context from Mem0: {str(e)}")
            return {}
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get a summary of the session"""
        try:
            # Get all interactions for the session
            interactions = self.client.get(
                key=f"session_{session_id}",
                include_metadata=True
            )
            
            if not interactions:
                return {"error": "No session data found"}
            
            # Extract relevant information
            summary = {
                "session_id": session_id,
                "total_interactions": len(interactions),
                "interaction_types": set(),
                "timestamps": [],
                "metadata": {}
            }
            
            for interaction in interactions:
                if isinstance(interaction, dict):
                    summary["interaction_types"].add(interaction.get("type", "unknown"))
                    if "timestamp" in interaction:
                        summary["timestamps"].append(interaction["timestamp"])
                    if "metadata" in interaction:
                        summary["metadata"].update(interaction["metadata"])
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting session summary from Mem0: {str(e)}")
            return {"error": str(e)}
    
    def clear_session(self, session_id: str) -> None:
        """Clear session data"""
        try:
            self.client.delete(key=f"session_{session_id}")
            logger.info(f"Successfully cleared session {session_id}")
        except Exception as e:
            logger.error(f"Error clearing session in Mem0: {str(e)}")
            raise 