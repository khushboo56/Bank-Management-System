CREATE DATABASE bank_reservation;

USE bank_reservation;

CREATE TABLE Customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    DateOfBirth DATE,
    ContactInformation VARCHAR(255),
    Address TEXT
);


CREATE TABLE Appointments (
    AppointmentID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    EmployeeID INT,
    ServiceType VARCHAR(255),
    AppointmentDateTime DATETIME,
    Status VARCHAR(20),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE BankEmployees (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Department VARCHAR(255)
);

CREATE TABLE Accounts (
    AccountID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    AccountType VARCHAR(255),
    AccountBalance DECIMAL(10, 2),
    Status VARCHAR(20),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE Transactions (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    AccountID INT,
    TransactionType VARCHAR(255),
    TransactionAmount DECIMAL(10, 2),
    TransactionDate DATETIME,
    FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
);

CREATE TABLE Loans (
    LoanID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    LoanType VARCHAR(255),
    LoanAmount DECIMAL(10, 2),
    LoanStatus VARCHAR(20),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

ALTER TABLE Customers
ADD COLUMN Username VARCHAR(255) UNIQUE,
ADD COLUMN Password VARCHAR(255);

UPDATE Customers
SET Username = 'default_username', Password = 'default_password'
WHERE Username IS NULL OR Password IS NULL;



DESCRIBE accounts;


-- Add the 'AccountType' column to the 'accounts' table if it doesn't exist
INSERT INTO accounts (AccountType) 
SELECT NULL 
FROM (SELECT 1) dummy
WHERE NOT EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_name = 'accounts' AND column_name = 'AccountType'
);

-- If the column was added, update the values
UPDATE accounts
SET AccountType = 'Savings'
WHERE AccountType IS NULL;



CREATE TABLE Customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) UNIQUE,
    Password VARCHAR(255),
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    DateOfBirth DATE,
    ContactInformation VARCHAR(255),
    Address TEXT
);

//new one customer table

DROP TABLE Loans;


CREATE TABLE LoanApplications (
    ApplicationID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    LoanAmount DECIMAL(10, 2),
    Status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    VerificationNotes TEXT,
    AdminNotes TEXT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);


ALTER TABLE Accounts
ADD AccountType ENUM('Savings', 'Current') NOT NULL;


CREATE TABLE SavingsAccounts (
    AccountID INT PRIMARY KEY,
    InterestRate DECIMAL(5, 4),
    FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
);

CREATE TABLE CurrentAccounts (
    AccountID INT PRIMARY KEY,
    OverdraftLimit DECIMAL(10, 2),
    FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
);

CREATE TABLE Admins (
    AdminID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Username VARCHAR(255) UNIQUE,
    Password VARCHAR(255)
);


