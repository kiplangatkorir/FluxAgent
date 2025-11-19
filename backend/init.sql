-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a table for general SQL queries (for SQL fetch tool)
CREATE TABLE IF NOT EXISTS sample_data (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    value INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some sample data
INSERT INTO sample_data (name, value) VALUES
    ('Item A', 100),
    ('Item B', 200),
    ('Item C', 150)
ON CONFLICT DO NOTHING;

