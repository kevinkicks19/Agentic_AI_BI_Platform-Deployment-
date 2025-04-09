from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
import json

class CoachAgent(BaseAgent):
    def __init__(self):
        system_message = """You are an expert Business Coach with deep expertise in:
        1. Problem Analysis and Understanding
        2. Business Process Improvement
        3. Strategic Planning
        4. Change Management
        5. Stakeholder Communication
        
        Your role is to:
        - Ask ONE focused question at a time
        - Wait for a response before asking the next question
        - Ensure you have a complete understanding of each aspect before moving on
        - Help users articulate their challenges clearly
        - Maintain a supportive and professional tone
        
        Follow these guidelines:
        1. Ask only ONE question at a time
        2. Make your question specific and focused
        3. Validate understanding before moving to the next topic
        4. Take notes of key information
        5. When you have sufficient information, summarize the problem and ask for confirmation
        6. Once confirmed, prepare a structured problem description for the routing agent"""
        
        super().__init__("Business_Coach", system_message)
        self.conversation_history: List[Dict[str, str]] = []
        self.problem_summary: Dict[str, Any] = {}
        self.current_topic: str = ""
        self.topics_to_cover = [
            "specific_challenge",
            "context_background",
            "goals_outcomes",
            "constraints_limitations",
            "stakeholders",
            "urgency_timeline",
            "requirements"
        ]
        self.current_topic_index = 0
    
    def is_conversation_complete(self) -> bool:
        """Check if the conversation has covered all required topics."""
        return self.current_topic_index >= len(self.topics_to_cover)
    
    async def conduct_discovery_conversation(self, conversation_state: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct a complete discovery conversation to understand the business problem.
        
        Args:
            conversation_state: Dictionary containing:
                - query: Initial problem description
                - context: Additional context information
        
        Returns:
            Dict[str, Any]: Results of the discovery conversation
        """
        # Initialize conversation with the query
        initial_response = await self.start_coaching(conversation_state["query"])
        
        # Simulate the conversation using the context
        context = conversation_state["context"]
        simulated_responses = [
            f"Our industry is {context.get('industry', 'unknown')}",
            f"Company size is {context.get('company_size', 'unknown')}",
            f"We're in the {context.get('product_type', 'unknown')} space",
            f"Current metrics: {', '.join(f'{k}={v}' for k, v in context.items() if 'rate' in k or 'lifetime' in k)}",
            f"Our main customer segment is {context.get('primary_customer_segment', 'unknown')}"
        ]
        
        # Process each simulated response
        for response in simulated_responses:
            await self.continue_coaching(response)
        
        # Generate problem summary
        summary = await self.prepare_routing_summary()
        
        # Structure the conversation results
        conversation_results = {
            "summary": summary,
            "conversation_history": self.conversation_history,
            "topics_covered": self.topics_to_cover[:self.current_topic_index],
            "key_insights": [
                {"topic": topic, "insight": next((msg["content"] for msg in self.conversation_history if topic in msg.get("metadata", {}).get("topic", "")), None)}
                for topic in self.topics_to_cover
            ],
            "metadata": {
                "total_exchanges": len(self.conversation_history),
                "completion_status": "completed" if self.is_conversation_complete() else "in_progress",
                "context_used": context
            }
        }
        
        return conversation_results
    
    async def start_coaching(self, initial_problem: str) -> str:
        """
        Start the coaching process with an initial problem description
        """
        self.conversation_history = []
        self.problem_summary = {}
        self.current_topic_index = 0
        
        prompt = f"""
        A user has presented the following business problem:
        {initial_problem}
        
        Please ask ONE focused question about the specific challenge they're facing.
        Make your question clear and specific, focusing on understanding the core issue.
        """
        
        response = await self.process_message(prompt, None)
        
        # Add to conversation history with metadata
        self.conversation_history.append({
            "role": "assistant",
            "content": response["content"],
            "metadata": {
                "topic": "specific_challenge",
                "type": "question"
            }
        })
        
        return response["content"]
    
    async def continue_coaching(self, user_response: str) -> str:
        """
        Continue the coaching process with the user's response
        """
        # Add user response to history with metadata
        self.conversation_history.append({
            "role": "user",
            "content": user_response,
            "metadata": {
                "topic": self.topics_to_cover[self.current_topic_index],
                "type": "response"
            }
        })
        
        # Move to next topic if we have enough information
        if len(self.conversation_history) >= 2:  # At least one exchange
            self.current_topic_index += 1
        
        # If we've covered all topics, prepare for summary
        if self.is_conversation_complete():
            prompt = f"""
            Based on the conversation history:
            {self.conversation_history}
            
            Please provide a summary of the problem and ask for confirmation.
            """
        else:
            # Ask the next question
            prompt = f"""
            Based on the conversation history:
            {self.conversation_history}
            
            Please ask ONE focused question about {self.topics_to_cover[self.current_topic_index]}.
            Make your question clear and specific.
            """
        
        response = await self.process_message(prompt, None)
        
        # Add to conversation history with metadata
        self.conversation_history.append({
            "role": "assistant",
            "content": response["content"],
            "metadata": {
                "topic": self.topics_to_cover[self.current_topic_index],
                "type": "question" if not self.is_conversation_complete() else "summary"
            }
        })
        
        return response["content"]
    
    async def prepare_routing_summary(self) -> Dict[str, Any]:
        """
        Prepare a structured summary of the problem for the routing agent
        """
        prompt = f"""
        Based on the conversation history:
        {self.conversation_history}
        
        Please prepare a structured summary of the problem that includes:
        1. Problem Statement
        2. Key Challenges
        3. Business Impact
        4. Stakeholders
        5. Constraints
        6. Desired Outcomes
        
        Format the summary as a JSON object with these fields.
        """
        
        response = await self.process_message(prompt, None)
        
        try:
            # Try to parse the response as JSON
            summary = json.loads(response["content"])
        except json.JSONDecodeError:
            # If parsing fails, create a basic structure
            summary = {
                "problem_statement": response["content"],
                "key_challenges": [],
                "business_impact": "",
                "stakeholders": [],
                "constraints": [],
                "desired_outcomes": []
            }
        
        return summary 