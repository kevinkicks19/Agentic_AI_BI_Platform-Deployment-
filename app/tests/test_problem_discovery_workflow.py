import pytest
import logging
import asyncio
from app.workflows.problem_discovery_workflow import ProblemDiscoveryWorkflow
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_problem_discovery_workflow():
    """Test the problem discovery workflow with a sample business problem."""
    logger.info("Starting problem discovery workflow test")
    
    # Initialize the workflow
    workflow = ProblemDiscoveryWorkflow(
        workflow_id="test_discovery",
        name="Test Problem Discovery",
        description="Test workflow for discovering and analyzing a business problem"
    )
    logger.info("Workflow initialized")
    
    # Sample input data
    input_data = {
        "initial_query": """
        Our company is experiencing high customer churn rates in our SaaS product. 
        We're losing about 15% of our customers every month, which is well above 
        industry standards. We need to understand why this is happening and develop 
        a comprehensive solution to improve customer retention.
        """,
        "user_context": {
            "industry": "SaaS",
            "company_size": "50-100 employees",
            "product_type": "B2B Software",
            "current_churn_rate": "15%",
            "target_churn_rate": "5%",
            "average_customer_lifetime": "6 months",
            "primary_customer_segment": "Small and Medium Businesses"
        }
    }
    logger.info("Input data prepared")
    
    try:
        # Execute the workflow with timeout
        logger.info("Starting workflow execution")
        async with asyncio.timeout(300):  # 5 minute timeout
            results = await workflow.execute(input_data)
            logger.info("Workflow execution completed")
        
        # Verify workflow completion
        assert workflow.status == "completed", "Workflow did not complete successfully"
        logger.info("Workflow status verified")
        
        # Check for required components in results
        assert "problem_summary" in results, "Missing problem summary"
        assert "solution_plan" in results, "Missing solution plan"
        assert "inception_document" in results, "Missing inception document"
        logger.info("Required components verified")
        
        # Generate plain text version of the inception document
        logger.info("Generating plain text document")
        plain_text_doc = generate_plain_text_document(results["inception_document"])
        
        # Save the document to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"inception_document_{timestamp}.txt"
        
        logger.info(f"Saving document to {filename}")
        with open(filename, "w") as f:
            f.write(plain_text_doc)
        
        logger.info(f"Generated inception document saved to: {filename}")
        
        # Print the document for review
        print("\nGenerated Inception Document:")
        print("=" * 80)
        print(plain_text_doc)
        print("=" * 80)
        
        return plain_text_doc
        
    except asyncio.TimeoutError:
        logger.error("Workflow execution timed out after 5 minutes")
        raise
    except Exception as e:
        logger.error(f"Error in problem discovery workflow: {str(e)}")
        raise

def generate_plain_text_document(inception_doc: dict) -> str:
    """Convert the inception document from JSON to a readable plain text format."""
    
    doc_sections = []
    
    # Title and Header
    doc_sections.append(f"{inception_doc['title']}\n{'=' * len(inception_doc['title'])}\n")
    doc_sections.append(f"Generated: {inception_doc['created_at']}\n")
    
    # Executive Summary
    doc_sections.append("Executive Summary\n----------------")
    exec_summary = inception_doc["sections"]["executive_summary"]
    doc_sections.append(f"\nProblem Statement:\n{exec_summary['problem_statement']}\n")
    doc_sections.append(f"\nProposed Solution:\n{exec_summary['proposed_solution']}\n")
    doc_sections.append("\nExpected Outcomes:")
    for outcome in exec_summary["expected_outcomes"]:
        doc_sections.append(f"- {outcome}")
    
    # Problem Analysis
    doc_sections.append("\n\nProblem Analysis\n---------------")
    prob_analysis = inception_doc["sections"]["problem_analysis"]
    doc_sections.append(f"\nContext:\n{prob_analysis['context']}\n")
    doc_sections.append("\nStakeholders:")
    for stakeholder in prob_analysis["stakeholders"]:
        doc_sections.append(f"- {stakeholder}")
    doc_sections.append("\nConstraints:")
    for constraint in prob_analysis["constraints"]:
        doc_sections.append(f"- {constraint}")
    doc_sections.append("\nSuccess Criteria:")
    for criterion in prob_analysis["success_criteria"]:
        doc_sections.append(f"- {criterion}")
    
    # Solution Approach
    doc_sections.append("\n\nSolution Approach\n----------------")
    solution = inception_doc["sections"]["solution_approach"]
    doc_sections.append(f"\nMethodology:\n{solution['methodology']}\n")
    doc_sections.append("\nRequired Agents:")
    for agent in solution["required_agents"]:
        doc_sections.append(f"- {agent}")
    doc_sections.append("\nTimeline:")
    for phase, time in solution["timeline"].items():
        doc_sections.append(f"- {phase}: {time}")
    doc_sections.append("\nDeliverables:")
    for deliverable in solution["deliverables"]:
        doc_sections.append(f"- {deliverable}")
    doc_sections.append("\nRisks and Mitigations:")
    for risk in solution["risks_mitigations"]:
        doc_sections.append(f"- {risk}")
    
    # Next Steps
    doc_sections.append("\n\nNext Steps\n----------")
    next_steps = inception_doc["sections"]["next_steps"]
    doc_sections.append("\nImmediate Actions:")
    for action in next_steps["immediate_actions"]:
        doc_sections.append(f"- {action}")
    doc_sections.append("\nResource Requirements:")
    for resource, requirement in next_steps["resource_requirements"].items():
        doc_sections.append(f"- {resource}: {requirement}")
    doc_sections.append("\nSuccess Metrics:")
    for metric in next_steps["success_metrics"]:
        doc_sections.append(f"- {metric}")
    
    # Join all sections
    return "\n".join(doc_sections)

if __name__ == "__main__":
    asyncio.run(test_problem_discovery_workflow()) 