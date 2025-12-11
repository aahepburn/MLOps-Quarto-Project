"""Simple batch model training with local artifact saving."""
import os
import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
import yaml
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, classification_report
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config(config_path='config/model_config.yaml'):
    """Load model configuration from YAML."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def load_data(file_path):
    """Load data from CSV file."""
    logger.info(f"Loading data from {file_path}")
    return pd.read_csv(file_path)


def train_model(X_train, y_train, config):
    """Train model with parameters from config."""
    params = config.get('model_params', {
        'n_estimators': 100,
        'max_depth': 10,
        'random_state': 42
    })
    
    logger.info(f"Training model with params: {params}")
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    """Evaluate model and return metrics."""
    y_pred = model.predict(X_test)
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'precision': float(precision_score(y_test, y_pred, average='weighted', zero_division=0)),
        'recall': float(recall_score(y_test, y_pred, average='weighted', zero_division=0)),
        'f1_score': float(f1_score(y_test, y_pred, average='weighted', zero_division=0))
    }
    
    # Add AUC if binary classification and predict_proba available
    if hasattr(model, 'predict_proba') and len(np.unique(y_test)) == 2:
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        metrics['roc_auc'] = float(roc_auc_score(y_test, y_pred_proba))
    
    return metrics


def save_model_and_metadata(model, metrics, config, model_dir='models/saved_models'):
    """Save model artifact and metadata JSON."""
    Path(model_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate version
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    version = f"v_{timestamp}"
    
    # Save model
    model_path = os.path.join(model_dir, f'model_{version}.pkl')
    joblib.dump(model, model_path)
    logger.info(f"Model saved to {model_path}")
    
    # Save as 'latest' for easy loading
    latest_path = os.path.join(model_dir, 'model_latest.pkl')
    joblib.dump(model, latest_path)
    logger.info(f"Model saved as latest: {latest_path}")
    
    # Save metadata
    metadata = {
        'version': version,
        'training_date': datetime.now().isoformat(),
        'model_type': 'RandomForestClassifier',
        'metrics': metrics,
        'parameters': config.get('model_params', {}),
        'features': config.get('features', []),
        'target': config.get('target', 'target'),
        'model_path': model_path
    }
    
    metadata_path = os.path.join(model_dir, f'metadata_{version}.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    logger.info(f"Metadata saved to {metadata_path}")
    
    # Save as 'latest' metadata
    latest_metadata_path = os.path.join(model_dir, 'metadata_latest.json')
    with open(latest_metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return version, model_path, metadata_path


def main():
    """Main training pipeline."""
    logger.info("="*60)
    logger.info("Starting Model Training Pipeline")
    logger.info("="*60)
    
    # Load config
    config = load_config()
    target_column = config.get('target', 'target')
    
    # Load data
    data_path = 'data/processed/train.csv'
    if not os.path.exists(data_path):
        logger.error(f"Training data not found: {data_path}")
        logger.info("Please ensure data/processed/train.csv exists")
        return
    
    data = load_data(data_path)
    logger.info(f"Loaded {len(data)} rows")
    
    # Check if target exists
    if target_column not in data.columns:
        logger.error(f"Target column '{target_column}' not found in data")
        logger.info(f"Available columns: {list(data.columns)}")
        logger.info(f"Update 'target' in config/model_config.yaml")
        return
    
    # Prepare features and target
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    logger.info(f"Features: {list(X.columns)}")
    logger.info(f"Target: {target_column}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    logger.info(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
    
    # Train model
    model = train_model(X_train, y_train, config)
    
    # Evaluate
    metrics = evaluate_model(model, X_test, y_test)
    
    logger.info("\n" + "="*60)
    logger.info("Model Performance Metrics")
    logger.info("="*60)
    for metric, value in metrics.items():
        logger.info(f"{metric}: {value:.4f}")
    
    # Save model and metadata
    version, model_path, metadata_path = save_model_and_metadata(
        model, metrics, config
    )
    
    logger.info("\n" + "="*60)
    logger.info("Training Complete!")
    logger.info("="*60)
    logger.info(f"Version: {version}")
    logger.info(f"Model: {model_path}")
    logger.info(f"Metadata: {metadata_path}")
    
    return {
        'version': version,
        'metrics': metrics,
        'model_path': model_path
    }


if __name__ == "__main__":
    result = main()
    if result:
        print(f"\n✅ Model trained successfully!")
        print(f"📊 Accuracy: {result['metrics']['accuracy']:.2%}")
        print(f"📦 Model: {result['model_path']}")