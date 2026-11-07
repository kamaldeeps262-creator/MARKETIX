-- MARKETIX PostgreSQL Database Schema

-- Drop tables if exists in reverse order of foreign keys
DROP TABLE IF EXISTS predictions CASCADE;
DROP TABLE IF EXISTS customer_segments CASCADE;
DROP TABLE IF EXISTS campaign_responses CASCADE;
DROP TABLE IF EXISTS campaigns CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS dataset_uploads CASCADE;

-- Table 1: customers
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    year_of_birth INTEGER,
    education VARCHAR(50),
    marital_status VARCHAR(50),
    income NUMERIC(12, 2),
    date_joined DATE,
    kidhome INTEGER DEFAULT 0,
    teenhome INTEGER DEFAULT 0,
    recency INTEGER,
    mnt_wines NUMERIC(10, 2) DEFAULT 0,
    mnt_fruits NUMERIC(10, 2) DEFAULT 0,
    mnt_meat NUMERIC(10, 2) DEFAULT 0,
    mnt_fish NUMERIC(10, 2) DEFAULT 0,
    mnt_sweets NUMERIC(10, 2) DEFAULT 0,
    mnt_gold NUMERIC(10, 2) DEFAULT 0,
    total_spending NUMERIC(12, 2) DEFAULT 0,
    num_deals_purchases INTEGER DEFAULT 0,
    num_web_purchases INTEGER DEFAULT 0,
    num_catalog_purchases INTEGER DEFAULT 0,
    num_store_purchases INTEGER DEFAULT 0,
    total_purchases INTEGER DEFAULT 0,
    num_web_visits_month INTEGER DEFAULT 0,
    complain INTEGER DEFAULT 0
);

-- Table 2: campaigns
CREATE TABLE IF NOT EXISTS campaigns (
    campaign_id INTEGER PRIMARY KEY,
    campaign_name VARCHAR(100) NOT NULL,
    campaign_type VARCHAR(50) DEFAULT 'Direct Marketing',
    start_date DATE,
    end_date DATE
);

-- Table 3: campaign_responses
CREATE TABLE IF NOT EXISTS campaign_responses (
    response_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id) ON DELETE CASCADE,
    campaign_id INTEGER REFERENCES campaigns(campaign_id) ON DELETE CASCADE,
    response BOOLEAN NOT NULL,
    response_date DATE,
    UNIQUE(customer_id, campaign_id)
);

-- Table 4: customer_segments
CREATE TABLE IF NOT EXISTS customer_segments (
    segment_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id) ON DELETE CASCADE,
    cluster_number INTEGER NOT NULL,
    segment_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 5: predictions
CREATE TABLE IF NOT EXISTS predictions (
    prediction_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id) ON DELETE CASCADE,
    predicted_response BOOLEAN NOT NULL,
    probability NUMERIC(5, 4) NOT NULL,
    model_version VARCHAR(50) DEFAULT 'v1.0-logreg',
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 6: dataset_uploads
CREATE TABLE IF NOT EXISTS dataset_uploads (
    upload_id SERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_records INTEGER NOT NULL,
    status VARCHAR(50) DEFAULT 'Processed'
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_customers_income ON customers(income);
CREATE INDEX IF NOT EXISTS idx_campaign_responses_cid ON campaign_responses(campaign_id);
CREATE INDEX IF NOT EXISTS idx_campaign_responses_custid ON campaign_responses(customer_id);
CREATE INDEX IF NOT EXISTS idx_segments_custid ON customer_segments(customer_id);
CREATE INDEX IF NOT EXISTS idx_predictions_custid ON predictions(customer_id);
