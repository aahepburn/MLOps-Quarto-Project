def create_features(df):
    # Example feature engineering: creating a new feature based on existing ones
    df['new_feature'] = df['feature1'] * df['feature2']  # Replace with actual feature logic
    return df

def encode_categorical_features(df, categorical_cols):
    # Example encoding of categorical features
    for col in categorical_cols:
        df[col] = df[col].astype('category').cat.codes
    return df

def scale_features(df, numeric_cols):
    # Example feature scaling
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df

def feature_engineering_pipeline(df):
    # Define the feature engineering pipeline
    df = create_features(df)
    categorical_cols = ['cat_feature1', 'cat_feature2']  # Replace with actual categorical columns
    df = encode_categorical_features(df, categorical_cols)
    numeric_cols = ['num_feature1', 'num_feature2']  # Replace with actual numeric columns
    df = scale_features(df, numeric_cols)
    return df