# MLOps Batch Model Project

A streamlined MLOps project demonstrating batch model training, versioning, and interactive dashboard visualization with Quarto.

## Overview

This project showcases a **batch-first MLOps approach**:
- Simple local model training with versioned artifacts
- JSON-based metadata tracking
- Interactive Quarto dashboard for model evaluation
- Automated deployment to GitHub Pages via CI/CD

**Philosophy**: Start simple, scale when needed. No complex infrastructure required.

## Quick Start (5 Minutes)

### 1. Clone and Install
```bash
git clone <repository-url>
cd mlops-quarto-project
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Prepare Your Data
```bash
# Add your training data
cp your_data.csv data/processed/train.csv

# Optionally add test data for dashboard
cp your_test_data.csv data/processed/test.csv
```

### 3. Configure Model
Edit `config/model_config.yaml`:
```yaml
model_params:
  n_estimators: 100
  max_depth: 10
  random_state: 42

features:
  - feature1
  - feature2
  # ... your actual feature names

target: "your_target_column"
```

### 4. Train Model
```bash
python src/models/train.py
```

This will:
- Train a RandomForestClassifier
- Save model to `models/saved_models/model_latest.pkl`
- Save metadata to `models/saved_models/metadata_latest.json`
- Display performance metrics

### 5. View Dashboard
```bash
cd dashboards
quarto preview dashboard.qmd
```

Open http://localhost:4200 to see your interactive dashboard!

## Project Structure

```
mlops-quarto-project/
├── .github/workflows/
│   └── ci-cd.yml              # CI/CD: tests + deploy dashboard
├── config/
│   ├── config.yaml
│   └── model_config.yaml      # Model hyperparameters
├── dashboards/
│   ├── dashboard.qmd          # Main interactive dashboard
│   └── deployment.qmd         # Documentation
├── data/
│   ├── raw/                   # Raw data
│   └── processed/             # Processed training/test data
├── models/
│   └── saved_models/          # Model artifacts + metadata
├── notebooks/
│   └── exploration.ipynb      # EDA notebook
├── src/
│   ├── data/
│   │   └── preprocessing.py
│   ├── features/
│   │   └── engineering.py
│   ├── models/
│   │   ├── train.py          # Simple training script
│   │   └── predict.py        # Prediction utilities
│   └── utils/
│       └── helpers.py
├── tests/
│   └── test_models.py
├── requirements.txt           # Minimal dependencies
└── README.md
```

## Workflow

### Local Development
```bash
# 1. Prepare data
python src/data/preprocessing.py

# 2. Train model
python src/models/train.py

# 3. Preview dashboard
cd dashboards && quarto preview dashboard.qmd

# 4. Run tests
pytest tests/ -v
```

### CI/CD (Automatic)
When you push to `main`:
1.  Run tests
2.  Render Quarto dashboard  
3.  Deploy to GitHub Pages

Access your dashboard at: `https://<username>.github.io/<repo-name>/`

##  Dashboard Features

The interactive dashboard shows:

### Model Overview
- Model version and training date
- Performance metrics (accuracy, precision, recall, F1)
- Hyperparameters used

### Predictions & Analysis
- Batch predictions on test set
- Prediction confidence distribution
- Confusion matrix
- Feature importance ranking

### Data Summary
- Dataset statistics
- KPI summary
- System status checks

## Configuration

### Model Parameters (`config/model_config.yaml`)
```yaml
model_params:
  n_estimators: 100      # Number of trees
  max_depth: 10          # Max tree depth
  min_samples_split: 2
  random_state: 42

features:
  - age                  # List your features
  - income
  - credit_score

target: "default"        # Your target column name
```

### Model Versioning
Models are automatically versioned with timestamps:
- `model_v_20241211_143022.pkl` - Timestamped version
- `model_latest.pkl` - Always points to latest
- `metadata_latest.json` - Model metadata

## Model Metadata Format

Each trained model generates a metadata JSON:
```json
{
  "version": "v_20241211_143022",
  "training_date": "2024-12-11T14:30:22",
  "model_type": "RandomForestClassifier",
  "metrics": {
    "accuracy": 0.8523,
    "precision": 0.8467,
    "recall": 0.8523,
    "f1_score": 0.8490,
    "roc_auc": 0.9123
  },
  "parameters": {
    "n_estimators": 100,
    "max_depth": 10,
    "random_state": 42
  },
  "features": ["feature1", "feature2", "..."],
  "target": "target_column"
}
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test
pytest tests/test_models.py -v
```

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute getting started guide
- **[dashboards/deployment.qmd](dashboards/deployment.qmd)** - Detailed setup guide
- **[SIMPLIFICATION_PLAN.md](SIMPLIFICATION_PLAN.md)** - Architecture decisions

## What Makes This MLOps?

Even though it's "batch-only", this demonstrates key MLOps principles:

**Versioned Artifacts**: Every model saved with metadata  
**Reproducibility**: Config-driven training  
**Monitoring**: Dashboard shows performance metrics  
**Automation**: CI/CD pipeline for deployment  
**Testing**: Automated test suite  
**Documentation**: Clear setup and usage guides

## Scaling Up (Optional)

When you need more, you can progressively add:

### Add Online API
- Restore `src/api/main.py` for FastAPI serving
- Deploy with Docker or Cloud Run
- Keep dashboard as monitoring tool

### Add Experiment Tracking
- Add MLflow for experiment tracking
- Compare multiple model versions
- Track hyperparameter tuning

### Add Cloud Infrastructure
- Store data in Cloud Storage
- Use Cloud SQL for predictions log
- Deploy with Terraform

**But start simple!** The current setup is production-ready for many use cases.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes and test: `pytest tests/`
4. Commit: `git commit -m "Add my feature"`
5. Push: `git push origin feature/my-feature`
6. Create Pull Request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- [Quarto](https://quarto.org/) - Interactive dashboards
- [Scikit-learn](https://scikit-learn.org/) - Machine learning
- [Plotly](https://plotly.com/) - Visualizations

