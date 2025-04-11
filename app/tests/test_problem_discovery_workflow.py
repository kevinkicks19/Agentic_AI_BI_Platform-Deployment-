import pytest
import os
import json
import logging
from datetime import datetime
from app.workflows.problem_discovery_workflow import ProblemDiscoveryWorkflow
from app.agents.user_simulation_agent import UserSimulationAgent
from app.agents.coach_agent import CoachAgent
from app.agents.router_agent import RouterAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.timeout(300)  # 5 minute timeout
def test_problem_discovery_workflow():
    """Test the problem discovery workflow with proper error handling and timeouts."""
    try:
        # Initialize workflow
        workflow = ProblemDiscoveryWorkflow()
        
        # Test data
        test_data = {
            "problem_description": "Our e-commerce platform is experiencing high cart abandonment rates",
            "user_profile": {
                "role": "e-commerce manager",
                "experience": "5 years in retail",
                "technical_knowledge": "intermediate",
                "goals": ["reduce cart abandonment", "improve conversion rates"]
            },
            "context": {
                "industry": "retail",
                "platform": "e-commerce",
                "user_base": "B2C"
            }
        }
        
        logger.info("Starting workflow execution...")
        # Execute workflow
        result = workflow.execute(test_data)
        
        logger.info("Workflow execution completed")
        
        # Verify results
        assert result["status"] == "success", f"Workflow failed with status: {result.get('status')}"
        assert "inception_document" in result, "No inception document in result"
        
        inception_doc = result["inception_document"]
        required_fields = ["timestamp", "problem_summary", "solution_plan", "conversation_summary", "metadata"]
        for field in required_fields:
            assert field in inception_doc, f"Missing required field: {field}"
        
        # Generate and save document
        try:
            doc_content = generate_plain_text_document(inception_doc)
            save_document(doc_content)
            logger.info("Document generated and saved successfully")
        except Exception as e:
            logger.error(f"Failed to generate or save document: {str(e)}")
            raise
            
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        raise

def test_workflow_input_validation():
    """Test input validation in the workflow"""
    workflow = ProblemDiscoveryWorkflow()
    
    # Test valid input
    valid_input = {
        "problem_description": "High cart abandonment rates on our e-commerce platform",
        "user_profile": {
            "name": "Test User",
            "role": "E-commerce Manager",
            "experience": "5 years in e-commerce",
            "goals": ["Reduce cart abandonment", "Improve conversion rates"]
        }
    }
    assert workflow.validate_input(valid_input) is True
    
    # Test missing required fields
    invalid_input = {
        "problem_description": "High cart abandonment rates"
    }
    assert workflow.validate_input(invalid_input) is False

def test_conversation_flow():
    """Test the conversation flow between agents"""
    workflow = ProblemDiscoveryWorkflow()
    user_agent = UserSimulationAgent({
        "name": "Test User",
        "role": "E-commerce Manager",
        "experience": "5 years in e-commerce",
        "goals": ["Reduce cart abandonment", "Improve conversion rates"]
    })
    coach_agent = CoachAgent()
    
    # Test initial message
    initial_message = "Hello! I'm here to help you explore your challenge. Could you tell me more about what you're facing?"
    user_response = user_agent.respond_to_coach(initial_message)
    assert isinstance(user_response, dict)
    assert "content" in user_response
    
    # Test coach response
    coach_response = coach_agent.continue_coaching(user_response["content"])
    assert isinstance(coach_response, str)
    assert len(coach_response) > 0

def test_workflow_execution():
    """Test the complete workflow execution"""
    workflow = ProblemDiscoveryWorkflow()
    
    # Prepare test input
    test_input = {
        "problem_description": "High cart abandonment rates on our e-commerce platform",
        "user_profile": {
            "name": "Test User",
            "role": "E-commerce Manager",
            "experience": "5 years in e-commerce",
            "goals": ["Reduce cart abandonment", "Improve conversion rates"]
        }
    }
    
    # Execute workflow
    result = workflow.execute(test_input)
    
    # Verify result structure
    assert isinstance(result, dict)
    assert "status" in result
    assert result["status"] == "success"
    
    # Verify inception document
    assert "inception_document" in result
    doc = result["inception_document"]
    assert isinstance(doc, dict)
    assert "timestamp" in doc
    assert "problem_summary" in doc
    assert "solution_plan" in doc
    assert "conversation_summary" in doc
    assert "metadata" in doc
    
    # Verify conversation history
    assert "conversation_history" in result
    assert isinstance(result["conversation_history"], list)
    assert len(result["conversation_history"]) > 0
    
    # Save the inception document
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    doc_path = f"inception_docs/inception_doc_{timestamp}.json"
    os.makedirs("inception_docs", exist_ok=True)
    
    with open(doc_path, "w") as f:
        json.dump(doc, f, indent=2)
    
    print(f"\nInception document saved to: {doc_path}")
    print("\nDocument contents:")
    print(json.dumps(doc, indent=2))

def generate_plain_text_document(inception_doc: dict) -> str:
    """Generate a plain text document from the inception document."""
    try:
        # Convert problem_summary to string if it's a dict
        problem_summary = inception_doc["problem_summary"]
        if isinstance(problem_summary, dict):
            problem_summary = "\n".join(f"{k}: {v}" for k, v in problem_summary.items())
            
        # Convert solution_plan to string if it's a dict
        solution_plan = inception_doc["solution_plan"]
        if isinstance(solution_plan, dict):
            solution_plan = "\n".join(f"{k}: {v}" for k, v in solution_plan.items())
            
        lines = [
            "PROBLEM DISCOVERY DOCUMENT",
            "========================",
            f"Generated: {inception_doc['timestamp']}",
            "\nPROBLEM SUMMARY",
            "--------------",
            problem_summary,
            "\nSOLUTION PLAN",
            "-------------",
            solution_plan,
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
    except KeyError as e:
        raise ValueError(f"Missing required field in inception document: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error generating document: {str(e)}")

def save_document(doc_content: str) -> str:
    """Save the document to the reports directory."""
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        logger.info(f"Created reports directory at: {os.path.abspath(reports_dir)}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(reports_dir, f"problem_discovery_{timestamp}.txt")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(doc_content)
    
    logger.info(f"Generated report saved to: {filename}")
    return filename

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 