from app.tools.tool_registry import tool_registry
from app.tools.data_analysis_tool import DataAnalysisTool
from app.tools.document_analysis_tool import DocumentAnalysisTool
from app.tools.business_metrics_tool import BusinessMetricsTool
from app.tools.web_search_tool import WebSearchTool

# Register all available tools
tool_registry.register_tool(DataAnalysisTool())
tool_registry.register_tool(DocumentAnalysisTool())
tool_registry.register_tool(BusinessMetricsTool())
tool_registry.register_tool(WebSearchTool())

# Export the tool registry
__all__ = ['tool_registry'] 