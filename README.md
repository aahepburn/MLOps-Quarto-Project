# MLOps Batch Model Project

A streamlined MLOps project demonstrating batch model training, versioning, and interactive dashboard visualization with Quarto.

## 🎯 Overview

This project showcases a **batch-first MLOps approach**:
- Simple local model training with versioned artifacts
- JSON-based metadata tracking
- Interactive Quarto dashboard for model evaluation
- Automated deployment to GitHub Pages via CI/CD

**Philosophy**: Start simple, scale when needed. No complex infrastructure required.

## 🚀 Quick Start (5 Minutes)

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

## 📁 Project Structure

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

## 🔄 Workflow

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
1. ✅ Run tests
2. 📊 Render Quarto dashboard  
3. 🚀 Deploy to GitHub Pages

Access your dashboard at: `https://<username>.github.io/<repo-name>/`

## 📊 Dashboard Features

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

## 🔧 Configuration

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

## 📈 Model Metadata Format

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

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test
pytest tests/test_models.py -v
```

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute getting started guide
- **[dashboards/deployment.qmd](dashboards/deployment.qmd)** - Detailed setup guide
- **[SIMPLIFICATION_PLAN.md](SIMPLIFICATION_PLAN.md)** - Architecture decisions

## 🎓 What Makes This MLOps?

Even though it's "batch-only", this demonstrates key MLOps principles:

✅ **Versioned Artifacts**: Every model saved with metadata  
✅ **Reproducibility**: Config-driven training  
✅ **Monitoring**: Dashboard shows performance metrics  
✅ **Automation**: CI/CD pipeline for deployment  
✅ **Testing**: Automated test suite  
✅ **Documentation**: Clear setup and usage guides

## 🚀 Scaling Up (Optional)

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes and test: `pytest tests/`
4. Commit: `git commit -m "Add my feature"`
5. Push: `git push origin feature/my-feature`
6. Create Pull Request

## 📝 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- [Quarto](https://quarto.org/) - Interactive dashboards
- [Scikit-learn](https://scikit-learn.org/) - Machine learning
- [Plotly](https://plotly.com/) - Visualizations

## 🏗️ Architecture Overview

This project demonstrates a complete MLOps pipeline with:

- **Data Layer**: Cloud-based storage (Cloud SQL PostgreSQL + Cloud Storage)
- **ML Training**: MLflow experiment tracking and model registry
- **Model Serving**: FastAPI REST API deployed on Cloud Run
- **Monitoring**: Automated drift detection and performance tracking
- **Dashboard**: Interactive Quarto dashboard with real-time metrics
- **CI/CD**: Automated deployment via GitHub Actions

## 🚀 Quick Start

### Local Development

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd mlops-quarto-project
   ```

2. **Start Local Infrastructure**
   ```bash
   # Start PostgreSQL, MLflow, and API services
   docker-compose up -d
   
   # Verify services are running
   docker-compose ps
   ```

3. **Install Python Dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   ```bash
   docker-compose exec postgres psql -U mlops -d mlops_data -f /docker-entrypoint-initdb.d/init.sql
   ```

5. **Access Services**
   - MLflow UI: http://localhost:5000
   - FastAPI Docs: http://localhost:8000/docs
   - MinIO Console: http://localhost:9001

### Train Your First Model

```bash
# Set environment variables
export MLFLOW_TRACKING_URI=http://localhost:5000
export DATABASE_URL=postgresql://mlops:mlops_dev_password@localhost:5432/mlops_data

# Run training pipeline
python src/models/train_mlflow.py
```

### Make Predictions

```bash
# Via API
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": {"feature1": 1.0, "feature2": 2.0}}'

# Or use Python
python -c "from src.models.predict import predict; print(predict('models/saved_models/model.pkl', data))"
```

### View Dashboard

```bash
cd dashboards
quarto preview dashboard.qmd
```

## 📁 Project Structure

```
mlops-quarto-project/
├── .github/workflows/          # CI/CD pipelines
│   ├── ci-cd.yml              # Main deployment pipeline
│   ├── train-model.yml        # Automated training
│   └── drift-monitoring.yml   # Daily drift detection
├── config/                     # Configuration files
│   ├── config.yaml
│   └── model_config.yaml
├── dashboards/                 # Quarto dashboards
│   ├── dashboard.qmd          # Main MLOps dashboard
│   ├── deployment.qmd         # Deployment guide
│   └── components/
├── data/                       # Data storage
│   ├── raw/                   # Raw data
│   ├── processed/             # Processed data
│   └── monitoring/            # Production monitoring data
├── infra/                      # Infrastructure as Code
│   ├── terraform/             # GCP infrastructure
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars.example
│   └── db/
│       └── init.sql           # Database schema
├── models/                     # Model artifacts
│   └── saved_models/
├── notebooks/                  # Jupyter notebooks
│   └── exploration.ipynb
├── scripts/                    # Utility scripts
│   ├── detect_drift.py        # Drift detection
│   ├── evaluate_model.py      # Model evaluation
│   └── ingest_data.py         # Data ingestion
├── src/                        # Source code
│   ├── api/
│   │   └── main.py            # FastAPI application
│   ├── data/
│   │   ├── preprocessing.py
│   │   └── data_access.py     # Database layer
│   ├── features/
│   │   └── engineering.py
│   ├── models/
│   │   ├── train.py
│   │   ├── train_mlflow.py    # MLflow training
│   │   └── predict.py
│   └── utils/
│       ├── helpers.py
│       └── mlflow_utils.py    # MLflow utilities
├── tests/                      # Unit tests
│   ├── __init__.py
│   └── test_models.py
├── docker-compose.yml          # Local services
├── Dockerfile                  # API container
├── .gitignore
├── requirements.txt
├── pyproject.toml
└── README.md
```

## 🌐 Cloud Deployment

### Prerequisites

1. GCP account with billing enabled
2. `gcloud` CLI installed and authenticated
3. Terraform installed (>= 1.0)
4. GitHub repository with secrets configured

### Required GitHub Secrets

```bash
GCP_SA_KEY           # Service account JSON key
GCP_PROJECT_ID       # Your GCP project ID
DATABASE_URL         # PostgreSQL connection string
MLFLOW_TRACKING_URI  # MLflow server URL
```

### Deploy Infrastructure

```bash
cd infra/terraform

# Configure variables
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# Deploy
terraform init
terraform plan
terraform apply
```

### Deploy API to Cloud Run

Push to `main` branch to trigger automatic deployment via GitHub Actions:

```bash
git add .
git commit -m "Deploy to production"
git push origin main
```

Or manually deploy:

```bash
# Build and push image
docker build -t gcr.io/PROJECT_ID/mlops-api:latest .
docker push gcr.io/PROJECT_ID/mlops-api:latest

# Deploy to Cloud Run
gcloud run deploy mlops-api \
  --image gcr.io/PROJECT_ID/mlops-api:latest \
  --region us-central1 \
  --platform managed
```

## 📊 Dashboard Features

The Quarto dashboard provides:

### Data & Model Status
- Current production model version and metadata
- Model performance metrics (accuracy, precision, recall, etc.)
- Latest data refresh timestamp
- System health status

### Performance Monitoring
- Prediction vs actual charts
- Confidence distribution analysis
- Model performance trends over time
- Recent predictions table

### Business Insights
- Key performance indicators (KPIs)
- Prediction volume analytics
- Model version usage statistics
- Automated alerts and warnings

### Drift Detection
- Feature-level drift indicators
- Statistical drift metrics (PSI, KS test)
- Threshold monitoring
- Visual drift reports

## 🔄 CI/CD Workflows

### Main Pipeline (`ci-cd.yml`)
**Triggers**: Push to main, pull requests
- Runs tests and linting
- Builds Docker image
- Deploys to Cloud Run
- Publishes dashboard to GitHub Pages

### Model Training (`train-model.yml`)
**Triggers**: Weekly schedule, manual
- Downloads training data from GCS
- Trains model with MLflow tracking
- Uploads artifacts to cloud storage
- Generates training report

### Drift Monitoring (`drift-monitoring.yml`)
**Triggers**: Daily schedule
- Downloads production data
- Runs drift detection analysis
- Generates drift report
- Sends alerts if drift detected

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/test_models.py -v
```

## 🔍 Monitoring & Observability

### Data Drift Detection

```bash
python scripts/detect_drift.py
```

Monitors:
- Population Stability Index (PSI)
- Kolmogorov-Smirnov test statistics
- Feature distribution changes
- Automated threshold alerts

### Model Evaluation

```bash
python scripts/evaluate_model.py
```

Provides:
- Comprehensive metrics (accuracy, precision, recall, F1, ROC-AUC)
- Confusion matrix
- Classification report
- Performance comparison across versions

## 📖 Documentation

- **[Deployment Guide](dashboards/deployment.qmd)**: Complete deployment instructions
- **[API Documentation](http://localhost:8000/docs)**: Interactive API docs
- **[MLflow UI](http://localhost:5000)**: Experiment tracking interface

## 🛠️ Troubleshooting

### API Not Starting
```bash
docker-compose logs api
docker-compose restart api
```

### Database Connection Issues
```bash
docker-compose exec postgres psql -U mlops -d mlops_data -c "SELECT 1;"
```

### Model Loading Errors
```bash
# Check MLflow models
curl http://localhost:5000/api/2.0/mlflow/registered-models/list

# Reload model via API
curl -X POST http://localhost:8000/model/reload
```

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and add tests
3. Run tests and linting: `pytest && black src && flake8 src`
4. Commit: `git commit -m "Add my feature"`
5. Push: `git push origin feature/my-feature`
6. Create a Pull Request

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🙏 Acknowledgments

Built with:
- [MLflow](https://mlflow.org/) - ML lifecycle management
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Quarto](https://quarto.org/) - Scientific publishing
- [Scikit-learn](https://scikit-learn.org/) - Machine learning
- [PostgreSQL](https://www.postgresql.org/) - Database
- [Google Cloud Platform](https://cloud.google.com/) - Cloud infrastructure