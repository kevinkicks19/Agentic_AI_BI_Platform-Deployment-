from typing import Dict, Any, List
import logging
from app.tools.base_tool import BaseTool

logger = logging.getLogger(__name__)

class BusinessMetricsTool(BaseTool):
    """Tool for calculating and analyzing business performance metrics."""
    
    def __init__(self):
        super().__init__(
            name="business_metrics",
            description="Calculate and analyze business performance metrics"
        )
        self.parameters = {
            "metric_type": {
                "type": "string",
                "description": "Type of metric to calculate",
                "required": True,
                "enum": ["financial", "customer", "operational", "marketing"]
            },
            "data": {
                "type": "object",
                "description": "Data required for the metric calculation",
                "required": True
            }
        }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the business metrics calculation."""
        if not self.validate_parameters(**kwargs):
            return {
                "status": "error",
                "error": "Invalid parameters"
            }
        
        try:
            metric_type = kwargs["metric_type"]
            data = kwargs["data"]
            
            if metric_type == "financial":
                return await self._calculate_financial_metrics(data)
            elif metric_type == "customer":
                return await self._calculate_customer_metrics(data)
            elif metric_type == "operational":
                return await self._calculate_operational_metrics(data)
            elif metric_type == "marketing":
                return await self._calculate_marketing_metrics(data)
            else:
                return {
                    "status": "error",
                    "error": f"Unknown metric type: {metric_type}"
                }
        
        except Exception as e:
            logger.error(f"Error calculating business metrics: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _calculate_financial_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate financial performance metrics."""
        revenue = data.get("revenue", 0)
        expenses = data.get("expenses", 0)
        assets = data.get("assets", 0)
        liabilities = data.get("liabilities", 0)
        
        return {
            "status": "success",
            "results": {
                "gross_profit": revenue - expenses,
                "profit_margin": (revenue - expenses) / revenue if revenue else 0,
                "roi": (revenue - expenses) / expenses if expenses else 0,
                "current_ratio": assets / liabilities if liabilities else 0
            }
        }
    
    async def _calculate_customer_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate customer-related metrics."""
        total_customers = data.get("total_customers", 0)
        new_customers = data.get("new_customers", 0)
        churned_customers = data.get("churned_customers", 0)
        revenue = data.get("revenue", 0)
        
        return {
            "status": "success",
            "results": {
                "customer_growth_rate": new_customers / total_customers if total_customers else 0,
                "churn_rate": churned_customers / total_customers if total_customers else 0,
                "customer_lifetime_value": revenue / total_customers if total_customers else 0,
                "net_promoter_score": data.get("nps_score", 0)
            }
        }
    
    async def _calculate_operational_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate operational efficiency metrics."""
        total_orders = data.get("total_orders", 0)
        completed_orders = data.get("completed_orders", 0)
        total_time = data.get("total_time", 0)
        resources_used = data.get("resources_used", 0)
        
        return {
            "status": "success",
            "results": {
                "order_fulfillment_rate": completed_orders / total_orders if total_orders else 0,
                "average_processing_time": total_time / completed_orders if completed_orders else 0,
                "resource_utilization": resources_used / data.get("total_resources", 1),
                "quality_score": data.get("quality_score", 0)
            }
        }
    
    async def _calculate_marketing_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate marketing performance metrics."""
        impressions = data.get("impressions", 0)
        clicks = data.get("clicks", 0)
        conversions = data.get("conversions", 0)
        revenue = data.get("revenue", 0)
        
        return {
            "status": "success",
            "results": {
                "click_through_rate": clicks / impressions if impressions else 0,
                "conversion_rate": conversions / clicks if clicks else 0,
                "cost_per_acquisition": data.get("marketing_cost", 0) / conversions if conversions else 0,
                "return_on_ad_spend": revenue / data.get("marketing_cost", 1)
            }
        } 