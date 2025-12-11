from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib
import os

def load_data(file_path):
    return pd.read_csv(file_path)

def train_model(data, target_column):
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    
    val_predictions = model.predict(X_val)
    accuracy = accuracy_score(y_val, val_predictions)
    
    return model, accuracy

def save_model(model, model_path):
    joblib.dump(model, model_path)

if __name__ == "__main__":
    data_file_path = os.path.join('data', 'processed', 'processed_data.csv')  # Adjust the path as necessary
    model_save_path = os.path.join('models', 'saved_models', 'random_forest_model.pkl')
    
    data = load_data(data_file_path)
    model, accuracy = train_model(data, target_column='target')  # Replace 'target' with the actual target column name
    save_model(model, model_save_path)
    
    print(f"Model trained with accuracy: {accuracy:.2f}")