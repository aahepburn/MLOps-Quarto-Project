"""Model prediction module with MLflow integration."""
import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ModelPredictor:
    """Model predictor with MLflow integration."""
    
    def __init__(self, mlflow_client=None):
        """Initialize predictor."""
        self.mlflow_client = mlflow_client
        self.model = None
        self.current_version = None
        self.current_run_id = None
        self.model_metadata = None
    
    async def load_production_model(self):
        """Load the current production model from MLflow."""
        if not self.mlflow_client:
            raise ValueError("MLflow client not initialized")
        
        model_info = await self.mlflow_client.get_latest_production_model()
        
        if not model_info:
            raise ValueError("No production model found")
        
        self.model = await self.mlflow_client.load_model(model_info["model_uri"])
        self.current_version = model_info["version"]
        self.current_run_id = model_info["run_id"]
        self.model_metadata = model_info
        
        logger.info(f"Loaded production model version {self.current_version}")
    
    async def load_model_version(self, version: str):
        """Load a specific model version."""
        if not self.mlflow_client:
            raise ValueError("MLflow client not initialized")
        
        model_info = await self.mlflow_client.get_model_by_version(version)
        
        if not model_info:
            raise ValueError(f"Model version {version} not found")
        
        self.model = await self.mlflow_client.load_model(model_info["model_uri"])
        self.current_version = model_info["version"]
        self.current_run_id = model_info["run_id"]
        self.model_metadata = model_info
        
        logger.info(f"Loaded model version {version}")
    
    async def predict(
        self,
        features: Dict[str, Any],
        model_version: Optional[str] = None
    ) -> Dict[str, Any]:
        """Make a prediction."""
        # Load specific version if requested
        if model_version and model_version != self.current_version:
            await self.load_model_version(model_version)
        
        if not self.model:
            raise ValueError("Model not loaded")
        
        # Convert features to appropriate format
        if isinstance(features, dict):
            feature_df = pd.DataFrame([features])
        else:
            feature_df = features
        
        # Make prediction
        prediction = self.model.predict(feature_df)
        
        # Get prediction probability if available
        confidence = None
        if hasattr(self.model, 'predict_proba'):
            proba = self.model.predict_proba(feature_df)
            confidence = float(np.max(proba))
        
        return {
            "prediction": prediction.tolist() if isinstance(prediction, np.ndarray) else prediction,
            "model_version": self.current_version,
            "model_run_id": self.current_run_id,
            "confidence": confidence
        }
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        if not self.model_metadata:
            raise ValueError("No model loaded")
        
        return {
            "model_name": os.getenv("MODEL_NAME", "mlops-model"),
            "model_version": self.current_version,
            "model_run_id": self.current_run_id,
            "training_date": self.model_metadata.get("tags", {}).get("training_date", "Unknown"),
            "metrics": self.model_metadata.get("metrics", {}),
            "parameters": self.model_metadata.get("params", {}),
            "is_production": self.model_metadata.get("stage") == "Production"
        }


def load_model(model_path):
    """Legacy function for loading model from file."""
    return joblib.load(model_path)


def make_predictions(model, input_data):
    """Legacy function for making predictions."""
    return model.predict(input_data)


def predict(model_path, input_data):
    """Legacy function for prediction pipeline."""
    model = load_model(model_path)
    predictions = make_predictions(model, input_data)
    return predictions