"""Simple tests for model training and prediction."""
import sys
from pathlib import Path
import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """Test that core modules can be imported."""
    from src.models import train
    from src.models import predict
    assert train is not None
    assert predict is not None


def test_train_functions_exist():
    """Test that training functions exist."""
    from src.models.train import load_config, train_model, evaluate_model
    assert callable(load_config)
    assert callable(train_model)
    assert callable(evaluate_model)


def test_predict_functions_exist():
    """Test that prediction functions exist."""
    from src.models.predict import load_model, make_predictions, predict
    assert callable(load_model)
    assert callable(make_predictions)
    assert callable(predict)


def test_config_loading():
    """Test configuration loading."""
    from src.models.train import load_config
    config = load_config()
    assert isinstance(config, dict)
    assert 'model_params' in config or 'target' in config
