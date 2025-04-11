import pytest
from litellm import completion
import os
from dotenv import load_dotenv

load_dotenv()

def test_litellm_openai_integration():
    """Test LiteLLM integration with OpenAI."""
    # Verify API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key is not None, "OPENAI_API_KEY not found in environment variables"
    
    # Test a simple completion
    try:
        response = completion(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello!"}
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        # Verify response structure
        assert response.choices is not None
        assert len(response.choices) > 0
        assert response.choices[0].message.content is not None
        
        print("\nLiteLLM OpenAI Integration Test Results:")
        print(f"Model: {response.model}")
        print(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        pytest.fail(f"LiteLLM OpenAI integration test failed: {str(e)}")

def test_platform_configuration():
    """Test platform configuration with LiteLLM."""
    from app.core.platform_config import PlatformConfig
    
    # Initialize platform config
    config = PlatformConfig()
    
    # Verify LLM configuration
    llm_config = config.get_config()["llm"]
    assert llm_config["provider"] == "openai"
    assert llm_config["model"] == "gpt-3.5-turbo"
    assert llm_config["api_key"] is not None
    
    print("\nPlatform Configuration Test Results:")
    print(f"LLM Provider: {llm_config['provider']}")
    print(f"Model: {llm_config['model']}")
    print("API Key: [REDACTED]") 