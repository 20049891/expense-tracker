CREATE DATABASE IF NOT EXISTS smart_expense_tracker;
USE smart_expense_tracker;

-- Users Table
CREATE TABLE IF NOT EXISTS User (
    userID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    income DECIMAL(15, 2) DEFAULT 0.00,
    role ENUM('USER', 'ADMIN') DEFAULT 'USER',
    status ENUM('ACTIVE', 'BLOCKED') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Expenses Table
CREATE TABLE IF NOT EXISTS Expense (
    expenseID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    date DATE NOT NULL,
    category VARCHAR(50) NOT NULL,
    mode ENUM('CASH', 'UPI', 'CARD', 'NET BANKING') DEFAULT 'CASH',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
);

-- Budgets Table
CREATE TABLE IF NOT EXISTS Budget (
    budgetID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    limitAmount DECIMAL(15, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE,
    UNIQUE KEY (userID, category)
);

-- Categories/Settings Table (Managed by Admin)
CREATE TABLE IF NOT EXISTS Category (
    categoryID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    icon VARCHAR(50) NOT NULL,
    is_default BOOLEAN DEFAULT FALSE
);

-- Reports Table
CREATE TABLE IF NOT EXISTS Report (
    reportID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT NOT NULL,
    type ENUM('MONTHLY', 'YEARLY') NOT NULL,
    dateRange VARCHAR(100) NOT NULL,
    file_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
);

-- AI Insights Table
CREATE TABLE IF NOT EXISTS AIInsights (
    insightID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT NOT NULL,
    type ENUM('PREDICTION', 'ALERT', 'INSIGHT') NOT NULL,
    message TEXT NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
);

-- Initial Data Setup: Admin user
INSERT IGNORE INTO User (name, email, password, role) VALUES ('Admin', 'admin@tracker.com', 'scrypt:32768:8:1$n4Bht1dO91qCqXzV$d5a1532ee0ceb770eedf3daef04fa057f5c5b4e3415e5ec1fd3b2b0fc891f63ac3f1af140130db17bcdf633f81eec9569ba7c5b651030e4df465389cb1f1bcf3', 'ADMIN');

-- Initial Data Setup: Default Categories
INSERT IGNORE INTO Category (name, icon, is_default) VALUES 
('Food', '🍔', TRUE),
('Travel', '🚗', TRUE),
('Shopping', '🛍️', TRUE),
('Bills', '🧾', TRUE),
('Entertainment', '🎬', TRUE),
('Healthcare', '⚕️', TRUE);
