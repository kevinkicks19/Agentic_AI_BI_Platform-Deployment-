from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timezone
import json
import requests
from app.config.settings import settings
import os

logger = logging.getLogger(__name__)

class PhoenixArizeIntegration:
    def __init__(self):
        """Initialize Phoenix Arize integration"""
        try:
            if not settings.ARIZE_API_KEY:
                raise ValueError("API key is required")
            
            # Set up API client
            self.api_key = settings.ARIZE_API_KEY
            self.base_url = "https://app.phoenix.arize.com/api/v1"
            
            # Split API key into parts and use the first part as username and combine the rest as password
            parts = self.api_key.split(":")
            if len(parts) < 2:
                raise ValueError("API key must have at least two parts separated by ':'")
            
            username = parts[0]
            password = ":".join(parts[1:])  # Join remaining parts as password
            self.auth = (username, password)
            
            self.headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            logger.info("Successfully initialized Phoenix Arize client")
        except Exception as e:
            logger.error(f"Error initializing Phoenix Arize client: {str(e)}")
            raise

    def log_prediction(self, 
                      model_name: str,
                      prediction: Dict[str, Any],
                      actual: Optional[Dict[str, Any]] = None,
                      metadata: Optional[Dict[str, Any]] = None) -> None:
        """Log a prediction event with optional actual values and metadata."""
        try:
            timestamp = metadata.get("timestamp") if metadata else None
            if not timestamp:
                timestamp = datetime.now(timezone.utc).isoformat()
            
            # Create a trace for the prediction
            inference_data = {
                "model_id": model_name,
                "trace_id": metadata.get("session_id", ""),
                "prompt": prediction.get("content", ""),
                "completion": prediction.get("content", ""),
                "model_version": prediction.get("model_version", "1.0.0"),
                "latency_ms": prediction.get("latency", 0),
                "token_count": prediction.get("tokens", 0),
                "confidence": prediction.get("confidence", 1.0),
                "ground_truth": actual.get("content", "") if actual else "",
                "accuracy": actual.get("accuracy", 1.0) if actual else 1.0,
                "relevance": actual.get("relevance_score", 1.0) if actual else 1.0,
                "environment": metadata.get("environment", "development") if metadata else "development",
                "user_id": metadata.get("user_id", "") if metadata else "",
                "timestamp": timestamp
            }
            
            # Log the inference using the API
            response = requests.post(
                f"{self.base_url}/inferences",
                headers=self.headers,
                auth=self.auth,
                json=inference_data
            )
            response.raise_for_status()
            
            logger.info(f"Successfully logged prediction for model {model_name}")
        except Exception as e:
            logger.error(f"Error logging prediction to Phoenix Arize: {str(e)}")
            raise

    def get_model_metrics(self, model_name: str) -> Dict[str, Any]:
        """Get performance metrics for a specific model."""
        try:
            # Get model performance metrics
            response = requests.get(
                f"{self.base_url}/models/{model_name}/metrics",
                headers=self.headers,
                auth=self.auth
            )
            response.raise_for_status()
            metrics = response.json()
            
            return {
                "model_name": model_name,
                "metrics": metrics,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting model metrics from Phoenix Arize: {str(e)}")
            return {"error": str(e)}

    def analyze_model_performance(self, model_name: str) -> Dict[str, Any]:
        """Analyze model performance metrics."""
        try:
            # Get detailed performance analysis
            response = requests.get(
                f"{self.base_url}/models/{model_name}/analysis",
                headers=self.headers,
                auth=self.auth
            )
            response.raise_for_status()
            analysis = response.json()
            
            return {
                "model_name": model_name,
                "analysis": analysis,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            logger.error(f"Error analyzing model performance in Phoenix Arize: {str(e)}")
            return {"error": str(e)}

    def export_metrics(self, model_name: str, filepath: str) -> None:
        """Export metrics to a JSON file."""
        try:
            # Get metrics for the specified time range
            metrics = self.get_model_metrics(model_name)
            
            # Export to file
            with open(filepath, 'w') as f:
                json.dump(metrics, f, indent=2)
            
            logger.info(f"Successfully exported metrics for {model_name} to {filepath}")
        except Exception as e:
            logger.error(f"Error exporting metrics: {str(e)}")
            raise

    def get_model_schema(self, model_name: str) -> Dict[str, Any]:
        """Get the schema for a specific model."""
        try:
            # Get model schema
            response = requests.get(
                f"{self.base_url}/models/{model_name}/schema",
                headers=self.headers,
                auth=self.auth
            )
            response.raise_for_status()
            schema = response.json()
            
            return {
                "model_name": model_name,
                "schema": schema,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting model schema from Phoenix Arize: {str(e)}")
            return {"error": str(e)}

    def get_model_predictions(self, 
                            model_name: str, 
                            start_time: Optional[datetime] = None,
                            end_time: Optional[datetime] = None) -> Dict[str, Any]:
        """Get predictions for a specific model within a time range."""
        try:
            if not start_time:
                start_time = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0)
            if not end_time:
                end_time = datetime.now(timezone.utc)
            
            # Get predictions
            params = {
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat()
            }
            response = requests.get(
                f"{self.base_url}/models/{model_name}/predictions",
                headers=self.headers,
                auth=self.auth,
                params=params
            )
            response.raise_for_status()
            predictions = response.json()
            
            return {
                "model_name": model_name,
                "predictions": predictions,
                "time_range": {
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat()
                }
            }
        except Exception as e:
            logger.error(f"Error getting model predictions from Phoenix Arize: {str(e)}")
            return {"error": str(e)} 