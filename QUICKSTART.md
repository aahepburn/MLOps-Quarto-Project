# Quick Start Guide

## Get Running in 5 Minutes

### 1. Install Dependencies (1 min)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Add Your Data (1 min)
```bash
# Copy your training data
cp your_data.csv data/processed/train.csv

# Optional: test data for dashboard
cp your_test_data.csv data/processed/test.csv
```

### 3. Update Config (1 min)
Edit `config/model_config.yaml`:
```yaml
model_params:
  n_estimators: 100
  max_depth: 10

features:
  - your_feature_1
  - your_feature_2

target: "your_target_column"
```

### 4. Train Model (1 min)
```bash
python src/models/train.py
```

You'll see:
```
Model trained with accuracy: 0.85
Model saved to models/saved_models/model_latest.pkl
```

### 5. View Dashboard (1 min)
```bash
cd dashboards
quarto preview dashboard.qmd
```

Open http://localhost:4200

## What You Get

✅ **Trained model** saved in `models/saved_models/`  
✅ **Model metadata** with metrics and parameters  
✅ **Interactive dashboard** showing predictions and analysis  
✅ **Ready for GitHub Pages** - just push to deploy

## Next Steps

### Run Tests
```bash
pytest tests/ -v
```

### Experiment with Parameters
Edit `config/model_config.yaml` and retrain:
```bash
python src/models/train.py
```

### Deploy Dashboard
Push to `main` branch - GitHub Actions will automatically:
1. Run tests
2. Render dashboard
3. Deploy to GitHub Pages

### Add More Features
- Create new features in `src/features/engineering.py`
- Update preprocessing in `src/data/preprocessing.py`
- Add custom metrics to dashboard

## Common Issues

### "Target column not found"
**Solution**: Update `target:` in `config/model_config.yaml` to match your data

### "Training data not found"
**Solution**: Ensure file is at `data/processed/train.csv`

### Dashboard shows "No model found"
**Solution**: Run `python src/models/train.py` first

### Import errors
**Solution**: Make sure virtual environment is activated and requirements installed

## Need Help?

- Full docs: [README.md](README.md)
- Architecture details: [SIMPLIFICATION_PLAN.md](SIMPLIFICATION_PLAN.md)
- Deployment guide: [dashboards/deployment.qmd](dashboards/deployment.qmd)
