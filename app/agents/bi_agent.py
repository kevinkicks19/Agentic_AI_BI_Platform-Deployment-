from app.agents.base_agent import BaseAgent

class BusinessIntelligenceAgent(BaseAgent):
    def __init__(self):
        system_message = """You are an expert Business Intelligence Analyst with deep knowledge in:
        1. Data Analysis and Interpretation
        2. Market Research and Competitive Analysis
        3. Financial Analysis and Forecasting
        4. Business Strategy and Planning
        5. Performance Metrics and KPIs
        
        Your role is to:
        - Analyze business data and provide actionable insights
        - Identify trends and patterns in business operations
        - Make data-driven recommendations for business improvement
        - Help in strategic decision-making processes
        - Provide clear and concise explanations of complex business concepts
        
        Always maintain a professional tone and focus on practical, implementable solutions."""
        
        super().__init__("BI_Analyst", system_message)
    
    async def analyze_data(self, data: dict, analysis_type: str) -> str:
        """
        Analyze business data based on the specified analysis type
        """
        prompt = f"""
        Please analyze the following business data for {analysis_type}:
        
        Data: {data}
        
        Provide a detailed analysis including:
        1. Key findings
        2. Trends identified
        3. Recommendations
        4. Potential risks and opportunities
        """
        
        return await self.process_message(prompt, None) 