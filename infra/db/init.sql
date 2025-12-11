-- Initialize MLOps database schema

-- Create mlflow database
CREATE DATABASE mlflow;

-- Connect to mlops_data database
\c mlops_data;

-- Create data tables
CREATE TABLE IF NOT EXISTS raw_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    data_source VARCHAR(255),
    data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_raw_data_timestamp ON raw_data(timestamp);
CREATE INDEX idx_raw_data_source ON raw_data(data_source);

-- Create predictions table
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    model_version VARCHAR(100) NOT NULL,
    model_run_id VARCHAR(255),
    input_data JSONB NOT NULL,
    prediction JSONB NOT NULL,
    confidence FLOAT,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_predictions_timestamp ON predictions(timestamp);
CREATE INDEX idx_predictions_model_version ON predictions(model_version);

-- Create model metadata table
CREATE TABLE IF NOT EXISTS model_metadata (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
    model_version VARCHAR(100) NOT NULL,
    model_run_id VARCHAR(255) UNIQUE,
    training_date TIMESTAMP NOT NULL,
    metrics JSONB,
    parameters JSONB,
    status VARCHAR(50) DEFAULT 'training',
    is_production BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_model_metadata_version ON model_metadata(model_version);
CREATE INDEX idx_model_metadata_production ON model_metadata(is_production);

-- Create data drift monitoring table
CREATE TABLE IF NOT EXISTS drift_metrics (
    id SERIAL PRIMARY KEY,
    feature_name VARCHAR(255) NOT NULL,
    metric_type VARCHAR(100) NOT NULL,
    metric_value FLOAT NOT NULL,
    threshold FLOAT,
    is_drift_detected BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_drift_metrics_timestamp ON drift_metrics(timestamp);
CREATE INDEX idx_drift_metrics_feature ON drift_metrics(feature_name);

-- Create performance monitoring table
CREATE TABLE IF NOT EXISTS model_performance (
    id SERIAL PRIMARY KEY,
    model_version VARCHAR(100) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value FLOAT NOT NULL,
    evaluation_date TIMESTAMP NOT NULL,
    dataset_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_performance_model_version ON model_performance(model_version);
CREATE INDEX idx_performance_date ON model_performance(evaluation_date);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for model_metadata
CREATE TRIGGER update_model_metadata_updated_at
    BEFORE UPDATE ON model_metadata
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data refresh metadata
CREATE TABLE IF NOT EXISTS data_refresh_log (
    id SERIAL PRIMARY KEY,
    refresh_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    records_processed INT,
    error_message TEXT,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_refresh_log_started ON data_refresh_log(started_at);
