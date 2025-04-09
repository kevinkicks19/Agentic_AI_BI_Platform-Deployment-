from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from datetime import datetime
import json

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
        
        response = await self.process_message(prompt, None)
        
        try:
            # Try to parse the response as JSON
            analysis = json.loads(response["content"])
        except json.JSONDecodeError:
            # If parsing fails, create a basic structure
            analysis = {
                "swot_analysis": {
                    "strengths": [],
                    "weaknesses": [],
                    "opportunities": [],
                    "threats": []
                },
                "pestle_analysis": {
                    "political": [],
                    "economic": [],
                    "social": [],
                    "technological": [],
                    "legal": [],
                    "environmental": []
                },
                "root_cause_analysis": {
                    "primary_causes": [],
                    "secondary_causes": [],
                    "underlying_factors": []
                },
                "stakeholder_analysis": {
                    "high_power_high_interest": [],
                    "high_power_low_interest": [],
                    "low_power_high_interest": [],
                    "low_power_low_interest": []
                },
                "impact_assessment": {
                    "high_value_low_complexity": [],
                    "high_value_high_complexity": [],
                    "low_value_low_complexity": [],
                    "low_value_high_complexity": []
                },
                "key_findings": response["content"]
            }
        
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
        
        response = await self.process_message(prompt, None)
        
        try:
            # Try to parse the response as JSON
            plan = json.loads(response["content"])
        except json.JSONDecodeError:
            # If parsing fails, create a basic structure
            plan = {
                "solution_strategy": {
                    "approach": response["content"],
                    "principles": [],
                    "success_criteria": []
                },
                "required_resources": {
                    "agents": [],
                    "tools": [],
                    "external_resources": []
                },
                "implementation_plan": {
                    "phases": [],
                    "timeline": {},
                    "dependencies": []
                },
                "risk_management": {
                    "risks": [],
                    "mitigation_strategies": [],
                    "contingency_plans": []
                },
                "resource_optimization": {
                    "allocation_strategy": "",
                    "parallel_activities": [],
                    "efficiency_opportunities": []
                },
                "success_metrics": {
                    "kpis": [],
                    "measurement_methodology": "",
                    "targets": {}
                },
                "monitoring_and_adjustment": {
                    "tracking_approach": "",
                    "review_points": [],
                    "adjustment_mechanisms": []
                }
            }
        
        # Structure the complete solution package
        solution_plan = {
            "problem_summary": problem_summary,
            "problem_analysis": problem_analysis,
            "solution_plan": plan,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "1.0",
                "status": "draft"
            }
        }
        
        return solution_plan
    
    async def validate_plan(self, solution_plan: Dict[str, Any]) -> bool:
        """Validate the solution plan for completeness and feasibility."""
        prompt = f"""
        Please validate the following solution plan:
        {solution_plan}
        
        Check for:
        1. Completeness of all required sections
        2. Logical consistency between sections
        3. Feasibility of proposed solutions
        4. Adequacy of risk management
        5. Realism of timelines and resource requirements
        6. Clarity of success metrics
        
        Return a JSON object with:
        - "is_valid": boolean indicating overall validity
        - "validation_points": list of specific validation checks
        - "issues_found": list of any issues identified
        - "recommendations": list of improvement suggestions
        """
        
        response = await self.process_message(prompt, None)
        
        try:
            # Try to parse the response as JSON
            validation_result = json.loads(response["content"])
            return validation_result.get("is_valid", False)
        except json.JSONDecodeError:
            # If parsing fails, assume the plan is valid
            return True
    
    async def optimize_plan(self, solution_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize the solution plan for efficiency and effectiveness."""
        prompt = f"""
        Please optimize the following solution plan:
        {solution_plan}
        
        Focus on:
        1. Resource efficiency
        2. Timeline optimization
        3. Risk reduction
        4. Cost effectiveness
        5. Implementation simplicity
        6. Scalability and flexibility
        
        Return a JSON object with:
        - "optimized_plan": the optimized version of the solution plan
        - "optimization_changes": list of specific changes made
        - "expected_improvements": list of expected benefits
        - "potential_risks": list of any new risks introduced
        """
        
        response = await self.process_message(prompt, None)
        
        try:
            # Try to parse the response as JSON
            optimization_result = json.loads(response["content"])
            return optimization_result.get("optimized_plan", solution_plan)
        except json.JSONDecodeError:
            # If parsing fails, return the original plan
            return solution_plan 