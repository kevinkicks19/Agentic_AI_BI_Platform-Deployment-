from typing import List, Dict, Any
import litellm
import logging
from datetime import datetime
import os
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAgent:
    def __init__(self, name: str, system_message: str):
        logger.info(f"Initializing {name} agent")
        self.name = name
        self.system_message = system_message
        self.model = os.getenv("DEFAULT_MODEL", "ollama/llama2")
        
        # Create logs directory if it doesn't exist
        self.logs_dir = "logs"
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
            logger.info(f"Created logs directory at {os.path.abspath(self.logs_dir)}")
        
        # Configure LiteLLM
        litellm.set_verbose = True
        litellm.success_callback = ["langfuse"]
        litellm.failure_callback = ["langfuse"]
    
    def _log_conversation(self, message: str, response: Dict[str, Any], is_error: bool = False):
        """Log conversation to a text file."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.logs_dir}/{self.name}_{timestamp}.txt"
            logger.info(f"Logging conversation to {filename}")
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"=== Conversation Log for {self.name} ===\n\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n\n")
                f.write("=== System Message ===\n")
                f.write(f"{self.system_message}\n\n")
                f.write("=== Input Message ===\n")
                f.write(f"{message}\n\n")
                
                if is_error:
                    f.write("=== Error ===\n")
                    f.write(f"{response.get('content', 'Unknown error')}\n")
                else:
                    f.write("=== Response ===\n")
                    f.write(f"{response.get('content', 'No response')}\n\n")
                    f.write("=== Metadata ===\n")
                    for key, value in response.get('metadata', {}).items():
                        f.write(f"{key}: {value}\n")
            
            logger.info(f"Successfully logged conversation to {filename}")
        except Exception as e:
            logger.error(f"Failed to log conversation: {str(e)}")
    
    async def process_message(self, message: str, sender: Any = None) -> Dict[str, Any]:
        """
        Process a message and return a response with metadata using LiteLLM
        """
        try:
            logger.info(f"{self.name} processing message: {message}")
            
            # Prepare messages for LiteLLM
            messages = [
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": message}
            ]
            
            # Make request using LiteLLM
            response = litellm.completion(
                model=self.model,
                messages=messages,
                temperature=0.7,
                top_p=0.9,
                max_tokens=4096,
                stop=["</s>", "[/INST]", "[INST]"]
            )
            
            # Extract content from response
            content = response.choices[0].message.content.strip()
            
            # Create response object
            result = {
                "status": "success",
                "content": content,
                "role": "assistant",
                "metadata": {
                    "model": self.model,
                    "response_time": response._response_ms,
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
            # Log the conversation
            self._log_conversation(message, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            error_response = {
                "status": "error",
                "content": str(e),
                "role": "system",
                "metadata": {"error": str(e)}
            }
            self._log_conversation(message, error_response, is_error=True)
            return error_response 