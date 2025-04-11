from typing import Dict, Any, List
import logging
import numpy as np
import pandas as pd
from app.tools.base_tool import BaseTool

logger = logging.getLogger(__name__)

class DataAnalysisTool(BaseTool):
    """Tool for performing basic statistical analysis on data."""
    
    def __init__(self):
        super().__init__(
            name="data_analysis",
            description="Perform statistical analysis on data"
        )
        self.parameters = {
            "data": {
                "type": "array",
                "description": "Array of numerical data to analyze",
                "required": True
            },
            "analysis_type": {
                "type": "string",
                "description": "Type of analysis to perform (descriptive, correlation, trend)",
                "required": True,
                "enum": ["descriptive", "correlation", "trend"]
            }
        }
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the data analysis."""
        if not self.validate_parameters(**kwargs):
            return {
                "status": "error",
                "error": "Invalid parameters"
            }
        
        try:
            data = kwargs["data"]
            analysis_type = kwargs["analysis_type"]
            
            if analysis_type == "descriptive":
                return self._descriptive_analysis(data)
            elif analysis_type == "correlation":
                return self._correlation_analysis(data)
            elif analysis_type == "trend":
                return self._trend_analysis(data)
            else:
                return {
                    "status": "error",
                    "error": f"Unknown analysis type: {analysis_type}"
                }
        
        except Exception as e:
            logger.error(f"Error performing data analysis: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _descriptive_analysis(self, data: List[float]) -> Dict[str, Any]:
        """Perform descriptive statistical analysis."""
        df = pd.Series(data)
        return {
            "status": "success",
            "results": {
                "mean": float(df.mean()),
                "median": float(df.median()),
                "std": float(df.std()),
                "min": float(df.min()),
                "max": float(df.max()),
                "quartiles": {
                    "q1": float(df.quantile(0.25)),
                    "q2": float(df.quantile(0.5)),
                    "q3": float(df.quantile(0.75))
                }
            }
        }
    
    def _correlation_analysis(self, data: List[List[float]]) -> Dict[str, Any]:
        """Perform correlation analysis between variables."""
        df = pd.DataFrame(data)
        correlation_matrix = df.corr()
        return {
            "status": "success",
            "results": {
                "correlation_matrix": correlation_matrix.to_dict(),
                "strong_correlations": self._find_strong_correlations(correlation_matrix)
            }
        }
    
    def _trend_analysis(self, data: List[float]) -> Dict[str, Any]:
        """Perform trend analysis on time series data."""
        df = pd.Series(data)
        trend = np.polyfit(range(len(data)), data, 1)
        return {
            "status": "success",
            "results": {
                "slope": float(trend[0]),
                "intercept": float(trend[1]),
                "trend_direction": "increasing" if trend[0] > 0 else "decreasing"
            }
        }
    
    def _find_strong_correlations(self, corr_matrix: pd.DataFrame, threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Find strong correlations in the correlation matrix."""
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr = corr_matrix.iloc[i, j]
                if abs(corr) >= threshold:
                    strong_correlations.append({
                        "variable1": corr_matrix.columns[i],
                        "variable2": corr_matrix.columns[j],
                        "correlation": float(corr)
                    })
        return strong_correlations 