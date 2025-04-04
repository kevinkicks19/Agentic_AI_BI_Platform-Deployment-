from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from datetime import datetime

class RouterAgent(BaseAgent):
    def __init__(self):
        system_message = """You are an expert Problem Router with deep knowledge of:
        1. Business Intelligence Tools and Methods
        2. Data Analysis Techniques
        3. Business Process Optimization
        4. Strategic Planning Tools
        5. Various Business Analysis Frameworks
        
        Your role is to:
        - Analyze problem descriptions using established frameworks (SWOT, PESTLE, Porter's Five Forces)
        - Select appropriate agents and tools for problem-solving
        - Create structured, framework-based solution plans
        - Ensure comprehensive risk assessment and mitigation
        - Optimize resource allocation and timeline planning
        - Define clear, measurable success metrics
        
        Available Agents and Tools:
        1. Business Intelligence Agent
           - Data analysis and visualization
           - Market research and competitive intelligence
           - Financial analysis and forecasting
           - Performance metrics and KPI tracking
           - Business reporting and dashboards
        
        2. Strategy Agent
           - Strategic planning and roadmapping
           - Competitive analysis and positioning
           - Business model evaluation and innovation
           - Growth strategy development
           - Market opportunity assessment
        
        3. Process Optimization Agent
           - Workflow analysis and mapping
           - Efficiency improvement planning
           - Process redesign and automation
           - Bottleneck identification and resolution
           - Change management planning
        
        4. Data Analysis Tools
           - Statistical analysis and modeling
           - Trend analysis and forecasting
           - Pattern recognition and clustering
           - Predictive analytics
           - Data quality assessment
        
        5. Project Management Tools
           - Timeline and milestone planning
           - Resource allocation optimization
           - Risk assessment and mitigation
           - Progress tracking and reporting
           - Stakeholder communication planning
        
        Follow these guidelines:
        1. Start with thorough framework-based analysis
        2. Consider multiple solution approaches
        3. Prioritize based on impact and feasibility
        4. Create detailed implementation roadmaps
        5. Include clear success metrics and KPIs
        6. Plan for continuous monitoring and adjustment"""
        
        super().__init__("Problem_Router", system_message)
    
    async def analyze_problem(self, problem_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Perform detailed analysis of the problem using business frameworks."""
        prompt = f"""
        Based on the following problem summary:
        {problem_summary}
        
        Please perform a comprehensive analysis using:
        1. SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats)
        2. PESTLE Analysis (Political, Economic, Social, Technological, Legal, Environmental)
        3. Root Cause Analysis (5 Whys or Fishbone Diagram)
        4. Stakeholder Analysis (Power/Interest Matrix)
        5. Impact Assessment (Business Value vs Implementation Complexity)
        
        For each framework:
        - Provide detailed analysis
        - Identify key insights
        - Note potential solution directions
        
        Format the response as a JSON object with each analysis as a separate section.
        Include a "key_findings" section summarizing the most important insights.
        """
        
        analysis = await self.process_message(prompt, None)
        return analysis
    
    async def create_solution_plan(self, problem_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive solution plan based on problem analysis."""
        # First, perform detailed problem analysis
        problem_analysis = await self.analyze_problem(problem_summary)
        
        # Then, create solution plan
        prompt = f"""
        Based on the problem analysis:
        {problem_analysis}
        
        Create a comprehensive solution plan including:
        
        1. Solution Strategy:
           - Overall approach and methodology
           - Key principles and guidelines
           - Success criteria and metrics
        
        2. Required Resources:
           - Agents and their specific roles
           - Tools and technologies needed
           - External resources or expertise required
        
        3. Implementation Plan:
           - Detailed phase breakdown
           - Specific deliverables for each phase
           - Timeline and milestones
           - Dependencies and critical path
        
        4. Risk Management:
           - Potential risks and their impact
           - Mitigation strategies
           - Contingency plans
        
        5. Resource Optimization:
           - Resource allocation strategy
           - Parallel vs sequential activities
           - Efficiency opportunities
        
        6. Success Metrics:
           - Key Performance Indicators (KPIs)
           - Measurement methodology
           - Target values and thresholds
        
        7. Monitoring and Adjustment:
           - Progress tracking approach
           - Review points and criteria
           - Adjustment mechanisms
        
        Format the response as a detailed JSON object with these sections.
        Include specific, measurable metrics and timelines wherever possible.
        """
        
        plan = await self.process_message(prompt, None)
        
        # Structure the complete solution package
        solution_plan = {
            "problem_summary": problem_summary,
            "problem_analysis": problem_analysis,
            "solution_plan": plan,
            "metadata": {
                "generated_at": datetime.utcnow(),
                "version": "2.0",
                "framework_version": "comprehensive"
            },
            "status": "ready_for_execution"
        }
        
        # Validate the plan before returning
        if await self.validate_plan(solution_plan):
            return solution_plan
        else:
            raise ValueError("Generated solution plan failed validation")
    
    async def validate_plan(self, solution_plan: Dict[str, Any]) -> bool:
        """Validate the solution plan for completeness and feasibility."""
        prompt = f"""
        Please validate the following solution plan:
        {solution_plan}
        
        Perform a comprehensive validation checking:
        
        1. Completeness:
           - All required components present
           - Sufficient detail in each section
           - Clear connections between sections
        
        2. Feasibility:
           - Realistic timelines and resource requirements
           - Appropriate skill level assumptions
           - Manageable complexity
        
        3. Risk Management:
           - Comprehensive risk identification
           - Effective mitigation strategies
           - Viable contingency plans
        
        4. Success Criteria:
           - Clear and measurable metrics
           - Realistic targets
           - Appropriate measurement methods
        
        5. Resource Allocation:
           - Efficient use of resources
           - Clear responsibilities
           - Manageable workload distribution
        
        6. Implementation Approach:
           - Logical sequence of activities
           - Well-defined dependencies
           - Clear phase transitions
        
        For each category:
        - Provide a pass/fail assessment
        - List any specific issues found
        - Suggest improvements if needed
        
        Respond with a JSON object containing:
        - validation_result: "VALID" or "INVALID"
        - category_results: {category: {status, issues, suggestions}}
        - overall_assessment: string
        """
        
        validation_result = await self.process_message(prompt, None)
        
        # Parse validation result and check if valid
        if isinstance(validation_result, dict):
            return validation_result.get("validation_result") == "VALID"
        return False
    
    async def optimize_plan(self, solution_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize the solution plan for efficiency and effectiveness."""
        prompt = f"""
        Please optimize the following solution plan:
        {solution_plan}
        
        Look for opportunities to:
        1. Parallelize activities
        2. Reduce resource requirements
        3. Shorten timeline
        4. Increase efficiency
        5. Enhance effectiveness
        
        Provide specific optimization recommendations and their impact.
        Return the optimized plan as a JSON object.
        """
        
        optimized_plan = await self.process_message(prompt, None)
        return optimized_plan 