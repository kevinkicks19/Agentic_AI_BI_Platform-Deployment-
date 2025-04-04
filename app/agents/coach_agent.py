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
    
    async def conduct_discovery_conversation(self, conversation_state: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct a complete discovery conversation to understand the business problem.
        
        Args:
            conversation_state: Dictionary containing:
                - query: Initial problem description
                - context: Additional context information
                - topics_covered: List of topics already covered
                - questions_asked: List of questions already asked
                - key_insights: List of key insights gathered
        
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
                "completion_status": "completed" if self.current_topic_index >= len(self.topics_to_cover) else "in_progress",
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
        if self.current_topic_index >= len(self.topics_to_cover):
            prompt = f"""
            Based on the conversation history:
            {self.conversation_history}
            
            Please provide a summary of the problem and ask for confirmation.
            Make sure to highlight the key points we've discussed.
            Format your response as a JSON object with:
            1. summary: A concise summary of the problem
            2. key_points: List of key points discussed
            3. confirmation_question: A question to confirm understanding
            """
        else:
            # Get the next topic to cover
            next_topic = self.topics_to_cover[self.current_topic_index]
            topic_prompts = {
                "specific_challenge": "Ask ONE focused question about the specific challenge they're facing.",
                "context_background": "Ask ONE focused question about the context and background of the situation.",
                "goals_outcomes": "Ask ONE focused question about their goals and desired outcomes.",
                "constraints_limitations": "Ask ONE focused question about any constraints or limitations.",
                "stakeholders": "Ask ONE focused question about key stakeholders involved.",
                "urgency_timeline": "Ask ONE focused question about the urgency and timeline.",
                "requirements": "Ask ONE focused question about any specific requirements."
            }
            
            prompt = f"""
            User's response: {user_response}
            
            {topic_prompts[next_topic]}
            Make your question specific and focused on this aspect.
            Format your response as a JSON object with:
            1. question: Your focused question
            2. topic: The current topic being discussed
            3. insights: Key insights from the user's last response
            """
        
        response = await self.process_message(prompt, None)
        
        # Add to conversation history with metadata
        self.conversation_history.append({
            "role": "assistant",
            "content": response["content"],
            "metadata": {
                "topic": self.topics_to_cover[min(self.current_topic_index, len(self.topics_to_cover) - 1)],
                "type": "question" if self.current_topic_index < len(self.topics_to_cover) else "summary"
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
        1. Problem Description
        2. Context and Background
        3. Goals and Desired Outcomes
        4. Constraints and Limitations
        5. Key Stakeholders
        6. Urgency and Timeline
        7. Any Specific Requirements
        
        Format this as a JSON object with these keys.
        Ensure each section is detailed and actionable.
        Include specific metrics and data points mentioned in the conversation.
        """
        
        response = await self.process_message(prompt, None)
        
        try:
            # Try to parse the response as JSON
            if isinstance(response, dict):
                summary = response.get("content", "{}")
            else:
                summary = response
                
            if isinstance(summary, str):
                summary = json.loads(summary)
            
            # Structure the summary
            self.problem_summary = {
                "problem_description": summary.get("problem_description", ""),
                "context_background": summary.get("context_background", ""),
                "goals_outcomes": summary.get("goals_outcomes", ""),
                "constraints_limitations": summary.get("constraints_limitations", ""),
                "stakeholders": summary.get("stakeholders", ""),
                "urgency_timeline": summary.get("urgency_timeline", ""),
                "requirements": summary.get("requirements", ""),
                "metadata": {
                    "conversation_length": len(self.conversation_history),
                    "topics_covered": self.topics_to_cover[:self.current_topic_index],
                    "completion_status": "completed" if self.current_topic_index >= len(self.topics_to_cover) else "in_progress"
                }
            }
        except json.JSONDecodeError:
            # If JSON parsing fails, structure the raw response
            self.problem_summary = {
                "problem_description": str(response),
                "metadata": {
                    "parsing_error": True,
                    "raw_response": response
                }
            }
        
        return self.problem_summary 