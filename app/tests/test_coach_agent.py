import pytest
from app.agents.coach_agent import CoachAgent
from app.tools.tool_registry import tool_registry
from app.tools.data_analysis_tool import DataAnalysisTool
from app.tools.document_analysis_tool import DocumentAnalysisTool
from app.tools.business_metrics_tool import BusinessMetricsTool
from app.tools.web_search_tool import WebSearchTool

@pytest.fixture
def register_tools():
    """Register all tools before the test."""
    tool_registry.register_tool(DataAnalysisTool())
    tool_registry.register_tool(DocumentAnalysisTool())
    tool_registry.register_tool(BusinessMetricsTool())
    tool_registry.register_tool(WebSearchTool())
    yield
    # Clean up after test
    tool_registry._tools.clear()

@pytest.mark.asyncio
async def test_coach_agent_with_tools(register_tools):
    # Initialize the coach agent
    coach = CoachAgent()
    
    # Test initial problem analysis
    initial_problem = """
    Our e-commerce platform is experiencing high cart abandonment rates (currently at 75%).
    We've tried implementing a simplified checkout process, but it hasn't improved the situation.
    Our conversion rate is 2.5% and average order value is $85.
    We need to reduce cart abandonment and increase conversions.
    """
    
    # Start coaching session
    response = await coach.start_coaching(initial_problem)
    print("\nInitial response:", response)
    
    # Simulate user responses
    user_responses = [
        "We're in the fashion retail industry with about 100,000 monthly visitors.",
        "Our target is to reduce cart abandonment to 50% within 3 months.",
        "We have a team of 5 developers and a budget of $50,000 for this project.",
        "Our main stakeholders are the marketing team, product team, and customer support.",
        "We need to implement changes within the next quarter."
    ]
    
    # Continue coaching with simulated responses
    for response in user_responses:
        coach_response = await coach.continue_coaching(response)
        print("\nCoach response:", coach_response)
    
    # Get final summary
    summary = await coach.prepare_routing_summary()
    print("\nFinal summary:", summary)
    
    # Verify that tools were used
    assert "analysis" in coach.conversation_history[0]["metadata"]
    assert "document_summary" in coach.conversation_history[0]["metadata"]["analysis"]
    assert "metrics" in coach.conversation_history[0]["metadata"]["analysis"]
    
    # Verify that the summary contains structured information
    assert "Problem Statement" in summary
    assert "Key Challenges" in summary
    assert "Business Impact" in summary
    assert "Stakeholders" in summary
    assert "Constraints" in summary
    assert "Desired Outcomes" in summary 