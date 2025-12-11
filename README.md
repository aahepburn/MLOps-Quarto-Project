# ml-quarto-project

This project is a data science and MLOps initiative that includes a Quarto dashboard for batch model scoring and a machine learning training pipeline. The project is structured to facilitate data processing, feature engineering, model training, and evaluation.

## Project Structure

```
ml-quarto-project
├── data
│   ├── raw
│   └── processed
├── src
│   ├── data
│   │   ├── __init__.py
│   │   └── preprocessing.py
│   ├── features
│   │   ├── __init__.py
│   │   └── engineering.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── train.py
│   │   └── predict.py
│   └── utils
│       ├── __init__.py
│       └── helpers.py
├── models
│   └── saved_models
├── notebooks
│   └── exploration.ipynb
├── dashboards
│   ├── dashboard.qmd
│   ├── master-styles.scss
│   └── components
│       ├── model_metrics.qmd
│       └── predictions.qmd
├── config
│   ├── config.yaml
│   └── model_config.yaml
├── tests
│   ├── __init__.py
│   └── test_models.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd ml-quarto-project
   ```

2. **Install Dependencies**
   It is recommended to use a virtual environment. You can create one using `venv` or `conda`.
   ```bash
   pip install -r requirements.txt
   ```

3. **Data Preparation**
   - Place your raw data files in the `data/raw` directory.
   - Run the preprocessing scripts in `src/data/preprocessing.py` to clean and transform the data.

4. **Feature Engineering**
   - Use the functions in `src/features/engineering.py` to create new features from the processed data.

5. **Model Training**
   - Train your machine learning model by executing the training pipeline in `src/models/train.py`.

6. **Model Predictions**
   - Use `src/models/predict.py` to make predictions with the trained model.

7. **Exploratory Data Analysis**
   - Utilize the Jupyter notebook located in `notebooks/exploration.ipynb` for EDA and visualizations.

8. **Quarto Dashboard**
   - Render the Quarto dashboard by running the `dashboards/dashboard.qmd` file to visualize batch model scoring results.

## Testing

- Unit tests for the model training and prediction functions can be found in `tests/test_models.py`. Run the tests to ensure the integrity of your code.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.