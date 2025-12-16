DROP DATABASE IF EXISTS awash_analytics;
CREATE DATABASE awash_analytics CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE awash_analytics;

-- Customers Table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(50),
    address VARCHAR(200),
    account_number BIGINT UNIQUE NOT NULL,
    account_type VARCHAR(100),
    balance_etb DECIMAL(15,2),
    home_branch VARCHAR(150),
    join_date DATE,
    INDEX idx_account (account_number),
    INDEX idx_branch (home_branch)
) ENGINE=InnoDB;

-- Transactions Table
CREATE TABLE transactions (
    transaction_id BIGINT PRIMARY KEY,
    account_number BIGINT NOT NULL,
    date DATETIME,
    amount_etb DECIMAL(15,2),
    channel VARCHAR(100),
    location VARCHAR(150),
    merchant VARCHAR(100),
    fraud_flag TINYINT DEFAULT 0,
    FOREIGN KEY (account_number) REFERENCES customers(account_number) ON DELETE CASCADE,
    INDEX idx_date (date),
    INDEX idx_amount (amount_etb),
    INDEX idx_fraud (fraud_flag),
    INDEX idx_channel (channel),
    INDEX idx_location (location)
) ENGINE=InnoDB;

-- Optional: View for quick fraud overview
CREATE VIEW vw_fraud_summary AS
SELECT 
    c.home_branch,
    t.channel,
    COUNT(*) AS total_transactions,
    SUM(t.fraud_flag) AS fraud_count,
    ROUND(AVG(t.amount_etb), 2) AS avg_amount_etb
FROM transactions t
JOIN customers c ON t.account_number = c.account_number
GROUP BY c.home_branch, t.channel;