import pytest
import asyncio
import os
from datetime import datetime
from app.workflows.problem_discovery_workflow import ProblemDiscoveryWorkflow

@pytest.mark.asyncio
async def test_problem_discovery_workflow():
    # Initialize workflow
    workflow = ProblemDiscoveryWorkflow()
    
    # Test data
    test_data = {
        "problem_description": "Our e-commerce platform is experiencing high cart abandonment rates",
        "context": {
            "industry": "retail",
            "platform": "e-commerce",
            "user_base": "B2C"
        }
    }
    
    # Execute workflow
    result = await workflow.execute(test_data)
    
    # Verify results
    assert result["status"] == "success"
    assert "inception_document" in result
    
    inception_doc = result["inception_document"]
    assert "timestamp" in inception_doc
    assert "problem_summary" in inception_doc
    assert "solution_plan" in inception_doc
    assert "conversation_summary" in inception_doc
    assert "metadata" in inception_doc
    
    # Generate plain text document
    doc_content = f"""Problem Discovery Report
Generated on: {inception_doc['timestamp']}

Problem Summary:
{inception_doc['problem_summary']}

Solution Plan:
{inception_doc['solution_plan']}

Conversation Summary:
{inception_doc['conversation_summary']}

Metadata:
- Workflow Version: {inception_doc['metadata']['workflow_version']}
- Agents Used: {', '.join(inception_doc['metadata']['agents_used'])}
- Conversation Turns: {inception_doc['metadata']['conversation_turns']}
"""
    
    # Create reports directory if it doesn't exist
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        print(f"\nCreated reports directory at: {os.path.abspath(reports_dir)}")
    
    # Save document
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(reports_dir, f"problem_discovery_{timestamp}.txt")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(doc_content)
    
    print(f"\nGenerated report saved to: {filename}")

def generate_plain_text_document(inception_doc: dict) -> str:
    """Generate a plain text document from the inception document."""
    lines = [
        "PROBLEM DISCOVERY DOCUMENT",
        "========================",
        f"Generated: {inception_doc['timestamp']}",
        "\nPROBLEM SUMMARY",
        "--------------",
        inception_doc["problem_summary"],
        "\nSOLUTION PLAN",
        "-------------",
        inception_doc["solution_plan"],
        "\nCONVERSATION SUMMARY",
        "-------------------",
        inception_doc["conversation_summary"],
        "\nMETADATA",
        "--------",
        f"Workflow Version: {inception_doc['metadata']['workflow_version']}",
        f"Agents Used: {', '.join(inception_doc['metadata']['agents_used'])}",
        f"Conversation Turns: {inception_doc['metadata']['conversation_turns']}"
    ]
    return "\n".join(lines)

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 