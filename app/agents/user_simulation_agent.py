from typing import Dict, Any, List
import logging
from app.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class UserSimulationAgent(BaseAgent):
    def __init__(self, user_profile: Dict[str, Any]):
        """
        Initialize the UserSimulationAgent with a user profile
        
        Args:
            user_profile: Dictionary containing user characteristics like:
                - role: User's role in the organization
                - industry: Industry they work in
                - pain_points: List of potential pain points
                - communication_style: How they typically communicate
                - technical_level: Their technical expertise level
        """
        system_message = f"""You are a simulated user with the following profile:
Role: {user_profile.get('role', 'Business User')}
Industry: {user_profile.get('industry', 'Technology')}
Technical Level: {user_profile.get('technical_level', 'Intermediate')}
Communication Style: {user_profile.get('communication_style', 'Direct and concise')}

Your pain points include:
{chr(10).join(f"- {point}" for point in user_profile.get('pain_points', []))}

When responding to the coach:
1. Be realistic and consistent with your profile
2. Provide relevant context about your situation
3. Express concerns and challenges naturally
4. Ask clarifying questions when needed
5. Be open to exploring solutions but maintain realistic constraints
"""
        super().__init__("UserSimulationAgent", system_message)
        self.user_profile = user_profile
        self.conversation_history = []
    
    def respond_to_coach(self, coach_message: str) -> Dict[str, Any]:
        """
        Generate a response to the coach's message based on the user profile
        
        Args:
            coach_message: The message from the coaching agent
            
        Returns:
            Dict containing the response and metadata
        """
        # Add coach's message to conversation history
        self.conversation_history.append({
            "role": "coach",
            "content": coach_message
        })
        
        # Prepare the prompt with conversation context
        prompt = f"""Previous conversation:
{chr(10).join(f"{msg['role'].title()}: {msg['content']}" for msg in self.conversation_history[-3:])}

Coach's latest message: {coach_message}

Based on your user profile and the conversation so far, provide a natural response that:
1. Addresses the coach's questions or points
2. Provides relevant context from your experience
3. Expresses any concerns or challenges
4. Asks clarifying questions if needed
5. Maintains consistency with your user profile

Your response:"""
        
        # Get response from the model
        response = self.process_message(prompt)
        
        # Add user's response to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": response["content"]
        })
        
        return response
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the full conversation history"""
        return self.conversation_history 