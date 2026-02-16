-- Initialize databases for microservices
CREATE DATABASE IF NOT EXISTS accounts_db;
CREATE DATABASE IF NOT EXISTS payments_db;
CREATE DATABASE IF NOT EXISTS ledger_db;
CREATE DATABASE IF NOT EXISTS user_profile_db;

-- Create schemas
\c fintech;

CREATE SCHEMA IF NOT EXISTS accounts;
CREATE SCHEMA IF NOT EXISTS payments;
CREATE SCHEMA IF NOT EXISTS ledger;
CREATE SCHEMA IF NOT EXISTS user_profile;
