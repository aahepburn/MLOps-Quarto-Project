"""Model training module with MLflow tracking."""
import os
import sys
from datetime import datetime
from pathlib import Path
import joblib
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import pandas as pd
import numpy as np
import yaml
import logging

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.mlflow_utils import MLflowClient
from src.data.data_access import DataAccess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """Model trainer with MLflow tracking."""
    
    def __init__(self, config_path: str = "config/model_config.yaml"):
        """Initialize trainer with configuration."""
        self.config = self._load_config(config_path)
        self.mlflow_client = None
        self.data_access = None
        self.model = None
        self.metrics = {}
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    async def setup(self):
        """Setup MLflow and database connections."""
        mlflow_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
        self.mlflow_client = MLflowClient(mlflow_uri)
        
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            self.data_access = DataAccess(database_url)
    
    def train_model(self, X_train, y_train, params: dict = None):
        """Train the model."""
        if params is None:
            params = self.config.get("model_params", {})
        
        logger.info("Training model with parameters:")
        logger.info(params)
        
        self.model = RandomForestClassifier(**params, random_state=42)
        self.model.fit(X_train, y_train)
        
        logger.info("Model training completed")
        return self.model
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate the model and compute metrics."""
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1] if hasattr(self.model, 'predict_proba') else None
        
        self.metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, average='weighted'),
            "recall": recall_score(y_test, y_pred, average='weighted'),
            "f1_score": f1_score(y_test, y_pred, average='weighted')
        }
        
        if y_pred_proba is not None:
            self.metrics["roc_auc"] = roc_auc_score(y_test, y_pred_proba)
        
        logger.info("Model evaluation metrics:")
        for metric, value in self.metrics.items():
            logger.info(f"  {metric}: {value:.4f}")
        
        return self.metrics
    
    async def log_to_mlflow(self, params: dict, artifacts_dir: str = None):
        """Log training run to MLflow."""
        if self.mlflow_client is None:
            raise ValueError("MLflow client not initialized")
        
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        # Prepare artifacts
        artifacts = {}
        if artifacts_dir:
            Path(artifacts_dir).mkdir(parents=True, exist_ok=True)
            
            # Save model
            model_path = Path(artifacts_dir) / "model.pkl"
            joblib.dump(self.model, model_path)
            artifacts["model"] = str(model_path)
        
        # Log to MLflow
        run_id = await self.mlflow_client.log_model_training(
            model=self.model,
            metrics=self.metrics,
            params=params,
            artifacts=artifacts
        )
        
        logger.info(f"Training logged to MLflow with run_id: {run_id}")
        return run_id
    
    async def save_to_database(self, model_version: str, run_id: str, params: dict):
        """Save model metadata to database."""
        if self.data_access is None:
            logger.warning("Database not configured, skipping metadata save")
            return
        
        await self.data_access.save_model_metadata(
            model_name=os.getenv("MODEL_NAME", "mlops-model"),
            model_version=model_version,
            model_run_id=run_id,
            training_date=datetime.utcnow(),
            metrics=self.metrics,
            parameters=params,
            is_production=False
        )
        
        logger.info(f"Model metadata saved to database")
    
    async def save_performance_metrics(self, model_version: str):
        """Save performance metrics to database."""
        if self.data_access is None:
            return
        
        for metric_name, metric_value in self.metrics.items():
            await self.data_access.log_performance_metric(
                model_version=model_version,
                metric_name=metric_name,
                metric_value=metric_value,
                dataset_type="test"
            )
    
    async def cleanup(self):
        """Cleanup connections."""
        if self.data_access:
            await self.data_access.close()


async def train_pipeline(data_path: str = "data/processed/train.csv"):
    """Main training pipeline."""
    logger.info("Starting training pipeline...")
    
    # Initialize trainer
    trainer = ModelTrainer()
    await trainer.setup()
    
    try:
        # Load data
        logger.info(f"Loading data from {data_path}")
        df = pd.read_csv(data_path)
        
        # Prepare features and target
        # Adjust based on your actual data structure
        X = df.drop('target', axis=1) if 'target' in df.columns else df
        y = df['target'] if 'target' in df.columns else None
        
        if y is None:
            raise ValueError("No target column found in data")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        logger.info(f"Training set size: {len(X_train)}")
        logger.info(f"Test set size: {len(X_test)}")
        
        # Get parameters
        params = trainer.config.get("model_params", {})
        
        # Train model
        trainer.train_model(X_train, y_train, params)
        
        # Evaluate model
        metrics = trainer.evaluate_model(X_test, y_test)
        
        # Log to MLflow
        run_id = await trainer.log_to_mlflow(
            params=params,
            artifacts_dir="models/saved_models"
        )
        
        # Save to database
        model_version = f"v_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        await trainer.save_to_database(model_version, run_id, params)
        await trainer.save_performance_metrics(model_version)
        
        logger.info("Training pipeline completed successfully!")
        logger.info(f"Model version: {model_version}")
        logger.info(f"Run ID: {run_id}")
        
        return {
            "model_version": model_version,
            "run_id": run_id,
            "metrics": metrics
        }
        
    finally:
        await trainer.cleanup()


if __name__ == "__main__":
    import asyncio
    
    # Run training pipeline
    result = asyncio.run(train_pipeline())
    print("\nTraining completed!")
    print(f"Model version: {result['model_version']}")
    print(f"Metrics: {result['metrics']}")
