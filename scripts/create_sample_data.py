"""Create sample datasets for testing the pipeline."""
import pandas as pd
import numpy as np
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)

# Create sample data
n_samples = 1000
data = {
    'feature1': np.random.randn(n_samples),
    'feature2': np.random.randn(n_samples),
    'feature3': np.random.randn(n_samples),
    'target': np.random.randint(0, 2, n_samples)
}

df = pd.DataFrame(data)

# Create directories
Path('data/processed').mkdir(parents=True, exist_ok=True)

# Split into train and test
train_df = df.sample(frac=0.8, random_state=42)
test_df = df.drop(train_df.index)

# Save datasets
train_df.to_csv('data/processed/train.csv', index=False)
test_df.to_csv('data/processed/test.csv', index=False)

print(f"✅ Created sample datasets:")
print(f"   Training: {len(train_df)} samples")
print(f"   Test: {len(test_df)} samples")
print(f"   Features: {list(data.keys())[:-1]}")
print(f"   Target: {list(data.keys())[-1]}")
