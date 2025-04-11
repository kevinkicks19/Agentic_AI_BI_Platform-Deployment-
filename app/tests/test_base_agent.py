import pytest
import os
from app.agents.base_agent import BaseAgent

@pytest.mark.asyncio
async def test_base_agent_message_processing():
    # Create a test agent
    agent = BaseAgent(
        name="TestAgent",
        system_message="You are a helpful test agent."
    )
    
    # Test processing a simple message
    response = await agent.process_message("Hello, how are you?")
    
    # Verify the response structure
    assert response["status"] == "success"
    assert isinstance(response["content"], str)
    assert response["role"] == "assistant"
    assert isinstance(response["metadata"], dict)
    
    # Verify metadata fields
    metadata = response["metadata"]
    assert "model" in metadata
    assert isinstance(metadata["model"], str)
    
    # Check if the response was logged
    log_files = os.listdir("logs")
    assert any(f.startswith("TestAgent_") for f in log_files) 