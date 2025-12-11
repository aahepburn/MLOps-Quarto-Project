def load_data(file_path):
    import pandas as pd
    return pd.read_csv(file_path)

def clean_data(df):
    df = df.dropna()  # Remove missing values
    df = df.reset_index(drop=True)  # Reset index after dropping
    return df

def transform_data(df):
    # Example transformation: Convert categorical variables to dummy variables
    df = pd.get_dummies(df, drop_first=True)
    return df

def preprocess_data(file_path):
    raw_data = load_data(file_path)
    cleaned_data = clean_data(raw_data)
    processed_data = transform_data(cleaned_data)
    return processed_data