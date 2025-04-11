import pytest
import asyncio
from datetime import datetime
from app.workflows.problem_discovery_workflow import ProblemDiscoveryWorkflow

@pytest.mark.asyncio
async def test_enhanced_problem_discovery():
    # Create sample user profile
    user_profile = {
        "role": "Data Analyst",
        "industry": "E-commerce",
        "technical_level": "Advanced",
        "communication_style": "Detailed and analytical",
        "pain_points": [
            "Difficulty in tracking customer behavior across multiple channels",
            "Challenges in integrating data from various sources",
            "Need for real-time analytics capabilities",
            "Struggling with data quality and consistency"
        ]
    }
    
    # Create input data
    input_data = {
        "problem_description": "We need to improve our customer analytics capabilities to better understand customer behavior and preferences across different channels.",
        "user_profile": user_profile
    }
    
    # Initialize and run workflow
    workflow = ProblemDiscoveryWorkflow()
    result = await workflow.execute(input_data)
    
    # Verify results
    assert result["status"] == "success"
    assert "inception_document" in result
    assert "conversation_history" in result
    
    # Check inception document structure
    doc = result["inception_document"]
    assert "problem_summary" in doc
    assert "solution_plan" in doc
    assert "conversation_summary" in doc
    assert "metadata" in doc
    
    # Check conversation history
    history = result["conversation_history"]
    assert len(history) > 0
    assert all("role" in msg and "content" in msg for msg in history)
    
    # Generate a readable report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"problem_discovery_report_{timestamp}.txt"
    
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write("=== Problem Discovery Report ===\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        
        f.write("=== Problem Summary ===\n")
        f.write(f"{doc['problem_summary']}\n\n")
        
        f.write("=== Solution Plan ===\n")
        f.write(f"{doc['solution_plan']}\n\n")
        
        f.write("=== Conversation Summary ===\n")
        f.write(f"{doc['conversation_summary']}\n\n")
        
        f.write("=== Full Conversation ===\n")
        for msg in history:
            f.write(f"{msg['role'].title()}: {msg['content']}\n\n")
    
    print(f"\nReport generated: {report_filename}")
    return result 