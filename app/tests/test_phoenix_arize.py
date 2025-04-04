import pytest
import logging
from app.integrations.phoenix_arize_integration import PhoenixArizeIntegration
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

def test_phoenix_arize_connection():
    """Test basic connection and operations with Phoenix Arize"""
    # Initialize the client
    client = PhoenixArizeIntegration()
    logger.info("Successfully initialized Phoenix Arize client")
    
    # Test model name
    test_model = "test_model"
    
    # Test logging a prediction
    test_prediction = {
        "content": "This is a test prediction",
        "confidence": 0.95,
        "model_version": "1.0.0",
        "latency": 150,  # ms
        "tokens": 100
    }
    
    test_actual = {
        "content": "This is a test actual response",
        "accuracy": 0.98,
        "relevance_score": 0.95
    }
    
    test_metadata = {
        "session_id": "test_session_123",
        "type": "test",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": "development",
        "user_id": "test_user"
    }
    
    # Log a test prediction
    client.log_prediction(
        model_name=test_model,
        prediction=test_prediction,
        actual=test_actual,
        metadata=test_metadata
    )
    logger.info("Successfully logged test prediction")
    
    # Get model metrics
    metrics = client.get_model_metrics(test_model)
    assert "error" not in metrics, f"Failed to get metrics: {metrics.get('error')}"
    logger.info("Successfully retrieved model metrics")
    
    # Get model schema
    schema = client.get_model_schema(test_model)
    assert "error" not in schema, f"Failed to get schema: {schema.get('error')}"
    logger.info("Successfully retrieved model schema")
    
    # Get recent predictions
    predictions = client.get_model_predictions(
        test_model,
        start_time=datetime.now(timezone.utc).replace(hour=0, minute=0, second=0),
        end_time=datetime.now(timezone.utc)
    )
    assert "error" not in predictions, f"Failed to get predictions: {predictions.get('error')}"
    logger.info("Successfully retrieved model predictions")
    
    logger.info("All Phoenix Arize tests completed successfully")

if __name__ == "__main__":
    test_phoenix_arize_connection() 