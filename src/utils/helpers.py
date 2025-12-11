def load_data(file_path):
    import pandas as pd
    return pd.read_csv(file_path)

def save_data(df, file_path):
    df.to_csv(file_path, index=False)

def log_message(message):
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.info(message)

def check_missing_values(df):
    return df.isnull().sum()

def encode_categorical(df, columns):
    for column in columns:
        df[column] = df[column].astype('category').cat.codes
    return df

def split_data(df, target_column, test_size=0.2, random_state=42):
    from sklearn.model_selection import train_test_split
    X = df.drop(columns=[target_column])
    y = df[target_column]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)