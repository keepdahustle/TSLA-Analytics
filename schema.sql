-- ============================================================================
-- TSLA Analytics Database Schema
-- PostgreSQL schema untuk import ke Supabase
-- Created: 2024
-- ============================================================================

-- ============================================================================
-- Table 1: tesla_stock_data
-- ============================================================================
CREATE TABLE IF NOT EXISTS tesla_stock_data (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    close FLOAT NOT NULL,
    high FLOAT NOT NULL,
    low FLOAT NOT NULL,
    open FLOAT NOT NULL,
    volume BIGINT NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    month INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_tesla_stock_date ON tesla_stock_data(date);
CREATE INDEX IF NOT EXISTS idx_tesla_stock_year ON tesla_stock_data(year);
CREATE INDEX IF NOT EXISTS idx_tesla_stock_year_quarter ON tesla_stock_data(year, quarter);

-- ============================================================================
-- Table 2: model_evaluation
-- ============================================================================
CREATE TABLE IF NOT EXISTS model_evaluation (
    id SERIAL PRIMARY KEY,
    model VARCHAR(50) NOT NULL UNIQUE,
    mae FLOAT NOT NULL,
    rmse FLOAT NOT NULL,
    mape_percentage FLOAT NOT NULL,
    r_squared FLOAT NOT NULL,
    dir_accuracy FLOAT NOT NULL,
    dir_precision FLOAT NOT NULL,
    dir_recall FLOAT NOT NULL,
    dir_f1 FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_model_eval_model ON model_evaluation(model);

-- ============================================================================
-- Table 3: predictions_sarima
-- ============================================================================
CREATE TABLE IF NOT EXISTS predictions_sarima (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    actual FLOAT NOT NULL,
    sarima_pred FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_sarima_date ON predictions_sarima(date);

-- ============================================================================
-- Table 4: predictions_prophet
-- ============================================================================
CREATE TABLE IF NOT EXISTS predictions_prophet (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    actual FLOAT NOT NULL,
    prophet_pred FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_prophet_date ON predictions_prophet(date);

-- ============================================================================
-- Table 5: api_logs (Optional - untuk monitoring API usage)
-- ============================================================================
CREATE TABLE IF NOT EXISTS api_logs (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INT NOT NULL,
    response_time_ms INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index untuk monitoring
CREATE INDEX IF NOT EXISTS idx_api_logs_created_at ON api_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_api_logs_endpoint ON api_logs(endpoint);

-- ============================================================================
-- Sample Data (Optional - uncomment untuk test data)
-- ============================================================================

-- Insert sample model evaluation data
INSERT INTO model_evaluation (model, mae, rmse, mape_percentage, r_squared, dir_accuracy, dir_precision, dir_recall, dir_f1)
VALUES 
    ('SARIMA', 8.45, 11.23, 2.34, 0.92, 0.68, 0.70, 0.65, 0.67),
    ('Prophet', 9.12, 12.01, 2.56, 0.90, 0.65, 0.68, 0.62, 0.65)
ON CONFLICT (model) DO NOTHING;

-- ============================================================================
-- Views (Optional - untuk memudahkan queries)
-- ============================================================================

-- View untuk get latest stock price
CREATE OR REPLACE VIEW v_latest_stock_price AS
SELECT 
    date,
    close,
    high,
    low,
    open,
    volume,
    year,
    quarter,
    month
FROM tesla_stock_data
ORDER BY date DESC
LIMIT 1;

-- View untuk get stock data summary
CREATE OR REPLACE VIEW v_stock_summary AS
SELECT 
    year,
    quarter,
    COUNT(*) as trading_days,
    MIN(low) as min_price,
    MAX(high) as max_price,
    AVG(close) as avg_price,
    SUM(volume) as total_volume
FROM tesla_stock_data
GROUP BY year, quarter
ORDER BY year DESC, quarter DESC;

-- View untuk get model performance comparison
CREATE OR REPLACE VIEW v_model_comparison AS
SELECT 
    model,
    mae,
    rmse,
    mape_percentage,
    r_squared,
    dir_accuracy,
    CASE 
        WHEN r_squared >= 0.90 THEN 'Excellent'
        WHEN r_squared >= 0.80 THEN 'Very Good'
        WHEN r_squared >= 0.70 THEN 'Good'
        ELSE 'Fair'
    END as performance_rating
FROM model_evaluation
ORDER BY r_squared DESC;

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
