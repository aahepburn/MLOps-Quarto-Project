# MLOps Project Simplification Plan

## Current State Analysis

### ✅ What's Actually Useful
1. **Project structure** - well organized
2. **Docker-compose setup** - good for local development
3. **Basic model training scaffold** - needs data/config updates
4. **Quarto dashboard framework** - needs simplification
5. **Documentation** - comprehensive but aspirational

### ⚠️ What's Overcomplicated/Aspirational
1. **FastAPI + Cloud Run deployment** - adds complexity, requires live infrastructure
2. **Terraform/GCP infrastructure** - full cloud setup, needs credentials/costs
3. **3 GitHub Actions workflows** - complex CI/CD for initial development
4. **MLflow with tracking server** - heavy dependency, might be overkill
5. **Async database layer** - sophisticated but unnecessary for batch
6. **Drift detection system** - advanced feature, premature optimization

### 🔴 What Won't Work Without Changes
1. **Model training** - expects specific data format/columns ('target')
2. **API endpoints** - hard dependency on MLflow + database
3. **Dashboard** - tries to query API that may not exist
4. **Config files** - placeholder values, not real parameters
5. **All cloud infrastructure** - needs real GCP project + credentials

---

## Option 1: Simplify to Batch-Only (Recommended for MVP)

### Philosophy
- **No online API** - pure batch scoring at render time
- **Minimal dependencies** - remove MLflow server, database, cloud infra
- **Local-first** - everything works on laptop
- **GitHub Pages deployment** - static dashboard only

### Files to DELETE
```
src/api/                        # Remove entire API module
src/data/data_access.py         # Remove async database layer
src/utils/mlflow_utils.py       # Remove if using simple versioning
infra/terraform/                # Remove cloud infrastructure
.github/workflows/train-model.yml
.github/workflows/drift-monitoring.yml
docker-compose.yml              # Or simplify to just Quarto
Dockerfile                      # Remove API container
```

### Files to SIMPLIFY
```
.github/workflows/ci-cd.yml     → Keep only: tests + render Quarto
dashboards/dashboard.qmd        → Remove API calls, use local data
requirements.txt                → Remove: fastapi, asyncpg, mlflow, terraform
src/models/train_mlflow.py      → Rename to train.py, remove MLflow
```

### Files to CREATE/UPDATE
```
src/models/train.py             → Simple training with joblib save
src/models/model_metadata.py    → Simple JSON metadata tracking
src/data/load_data.py           → Simple data loading utilities
dashboards/dashboard.qmd        → Load model + data, compute metrics inline
config/model_config.yaml        → Real hyperparameters for your use case
```

### Simplified Architecture
```
User → GitHub push → Tests run → Quarto renders → GitHub Pages
                                    ↓
                               Loads model.pkl
                               Loads test data
                               Computes metrics
                               Shows charts
```

---

## Option 2: Keep API but Simplify Cloud

### Philosophy
- **Keep FastAPI** for "online" serving story
- **Local-first with optional cloud** 
- **Simplified MLflow** - file-based tracking, no server
- **Remove expensive pieces** - no Cloud SQL, simpler storage

### Files to DELETE
```
infra/terraform/                # Remove terraform, use manual setup
src/data/data_access.py         # Remove async database layer
.github/workflows/train-model.yml
.github/workflows/drift-monitoring.yml
infra/db/init.sql               # No database
```

### Files to SIMPLIFY
```
docker-compose.yml              → Keep only: mlflow + api (remove postgres)
src/api/main.py                 → Remove database dependencies
src/models/train_mlflow.py      → Keep MLflow but file-based
src/utils/mlflow_utils.py       → Simplify to local file tracking
.github/workflows/ci-cd.yml     → Simplify deployment
```

### Simplified Architecture
```
Local:
  Training → MLflow (file) → model.pkl saved
  API → FastAPI loads model.pkl
  Dashboard → Calls local API or loads files

Cloud (optional):
  Docker image → Cloud Run (just API, no database)
  Dashboard → GitHub Pages
```

---

## Option 3: Keep Full Stack but Make it Work

### Philosophy
- **Keep everything** but fix the placeholders
- **Real configuration** for your actual use case
- **Progressive setup** - local first, then cloud

### Critical Fixes Needed

#### 1. Model Training (`src/models/train_mlflow.py`)
**Issues:**
- Expects 'target' column (line 185)
- Hard-coded train.csv path (line 177)
- Assumes classification (roc_auc_score)

**Fix:**
```python
# Update config/model_config.yaml with REAL:
- feature names from your data
- target column name
- hyperparameters you want to tune

# Update train_mlflow.py:
- Replace hard-coded 'target' with config['target']
- Make data loading flexible
- Handle regression vs classification
```

#### 2. Config Files
**Issues:**
- Placeholder values everywhere
- No real hyperparameters

**Fix:**
```yaml
# config/model_config.yaml - REAL VALUES:
model_params:
  n_estimators: 100
  max_depth: 10
  min_samples_split: 2
  random_state: 42

features:
  - age
  - income
  - credit_score
  # ... your actual features

target: "default"  # your actual target
```

#### 3. API Startup (`src/api/main.py`)
**Issues:**
- Will fail if MLflow empty
- No fallback for missing model

**Fix:**
```python
# Add graceful degradation:
try:
    await predictor.load_production_model()
except Exception as e:
    logger.warning("No production model, using latest local")
    predictor.load_from_file("models/saved_models/latest.pkl")
```

#### 4. Dashboard (`dashboards/dashboard.qmd`)
**Issues:**
- Assumes API is running
- Hard-coded to async/API calls

**Fix:**
```python
# Add fallback to local files:
try:
    response = requests.get(API_URL)
except:
    # Fallback to local model/data
    model = joblib.load("models/saved_models/latest.pkl")
```

#### 5. Terraform (`infra/terraform/*.tf`)
**Issues:**
- No project ID
- Hard-coded names
- No state backend

**Fix:**
```hcl
# terraform.tfvars:
project_id = "your-actual-gcp-project"
region = "us-central1"
db_password = "use-secret-manager-here"
```

---

## Concrete Next Steps by Option

### For Option 1 (Batch-Only) - 2 hours
1. **Delete unnecessary files** (5 min)
   ```bash
   rm -rf src/api infra/terraform .github/workflows/train-model.yml
   rm src/data/data_access.py src/utils/mlflow_utils.py
   ```

2. **Simplify training** (30 min)
   - Copy `train.py` content, remove MLflow
   - Add simple metadata JSON save
   - Test with toy data

3. **Fix dashboard** (45 min)
   - Remove all API calls
   - Load model with joblib
   - Compute metrics inline
   - Test local render

4. **Update docs** (15 min)
   - README: remove cloud/API sections
   - Add simple quickstart

5. **Test end-to-end** (30 min)
   - Train on sample data
   - Render dashboard
   - Commit and verify GitHub Pages

### For Option 2 (Simple API) - 4 hours
1. **Clean up infrastructure** (20 min)
   - Remove Terraform
   - Simplify docker-compose
   
2. **Fix API** (1 hour)
   - Remove database dependencies
   - Add file-based model loading
   - Test health endpoint

3. **Simplify MLflow** (1 hour)
   - Switch to file-based tracking
   - Update training script
   - Test experiment logging

4. **Update dashboard** (1 hour)
   - Add API fallback to local files
   - Test both modes
   
5. **CI/CD** (1 hour)
   - Simplify to tests + render
   - Add optional Docker build

### For Option 3 (Full Stack) - 8+ hours
1. **Data preparation** (2 hours)
   - Get real training data
   - Document schema
   - Update configs

2. **Fix training pipeline** (2 hours)
   - Update for your data
   - Test locally
   - Verify MLflow tracking

3. **Local infrastructure** (2 hours)
   - Start docker-compose
   - Initialize database
   - Load sample data

4. **API testing** (1 hour)
   - Test all endpoints
   - Fix errors
   - Document API

5. **Cloud setup** (1+ hours)
   - Create GCP project
   - Run Terraform
   - Deploy and test

---

## Recommendation

**Start with Option 1** (Batch-Only), then optionally grow into Option 2/3.

### Why?
1. **Fastest to working prototype** - 2 hours vs 4-8 hours
2. **Lowest complexity** - fewer moving parts
3. **No cloud costs** - everything local + GitHub Pages
4. **Still impressive** - Quarto dashboard with real ML is enough
5. **Easy to upgrade** - can add API/cloud later if needed

### What You Get
- ✅ Working ML training pipeline
- ✅ Versioned model artifacts
- ✅ Interactive dashboard with real metrics
- ✅ Auto-deployed to GitHub Pages
- ✅ CI/CD with tests
- ✅ Professional documentation

### What You Skip (for now)
- ⏸️ Online API serving
- ⏸️ Cloud infrastructure
- ⏸️ Database integration
- ⏸️ MLflow tracking server
- ⏸️ Automated retraining

---

## How to Execute the Simplification

Want me to:
1. **Execute Option 1** - Delete files, simplify code, make it work?
2. **Execute Option 2** - Keep API, simplify infrastructure?
3. **Just fix Option 3** - Keep everything but fix the placeholders?

I can do any of these programmatically. Which path do you prefer?
