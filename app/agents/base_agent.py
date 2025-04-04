from typing import List, Dict, Any
import autogen
from app.config.settings import settings
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAgent:
    def __init__(self, name: str, system_message: str):
        logger.info(f"Initializing {name} agent")
        self.name = name
        self.system_message = system_message
        self.agent = autogen.AssistantAgent(
            name=name,
            system_message=system_message,
            llm_config={
                "config_list": [
                    {
                        "model": "llama2:latest",
                        "api_type": "ollama"
                    }
                ],
                "timeout": 60  # Add timeout
            },
            code_execution_config={"use_docker": False}
        )
        self.executor = ThreadPoolExecutor(max_workers=1)
    
    async def process_message(self, message: str, sender: Any) -> Dict[str, Any]:
        """
        Process a message and return a response with metadata
        """
        try:
            logger.info(f"{self.name} processing message: {message}")
            
            # Initialize chat
            chat_initiator = autogen.UserProxyAgent(
                name="user",
                human_input_mode="NEVER",
                max_consecutive_auto_reply=1,  # Limit to one response
                code_execution_config={"use_docker": False}
            )
            
            # Run chat in thread pool
            logger.info("Starting chat interaction in thread pool")
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                self.executor,
                lambda: chat_initiator.initiate_chat(
                    self.agent,
                    message=message,
                    sender=sender
                )
            )
            
            # Get response
            last_message = chat_initiator.last_message()
            logger.info(f"Got response: {last_message}")
            
            # Extract the actual response content
            content = last_message.get("content", "No response content")
            if isinstance(content, str):
                # Clean up the response if needed
                content = content.strip()
                # Remove any [INST] tags
                content = content.split('[INST')[0].strip()
                # Remove any control characters
                content = ''.join(char for char in content if ord(char) >= 32 or char in '\n\r\t')
            
            return {
                "status": "success",
                "content": content,
                "role": last_message.get("role", "assistant"),
                "metadata": {
                    "timestamp": last_message.get("timestamp", None),
                    "type": last_message.get("type", "message")
                }
            }
            
        except Exception as e:
            logger.error(f"Error in process_message: {str(e)}")
            return {
                "status": "error",
                "content": f"Error processing message: {str(e)}",
                "role": "system",
                "metadata": {
                    "error": str(e)
                }
            } 