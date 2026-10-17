-- Database creation script: runs automatically when the app starts.
-- Safe to run many times (IF NOT EXISTS).
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);
