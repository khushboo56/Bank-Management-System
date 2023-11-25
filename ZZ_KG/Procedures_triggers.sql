DELIMITER //
CREATE PROCEDURE CreateAppointment(
    IN p_CustomerID INT,
    IN p_EmployeeID INT,
    IN p_ServiceType VARCHAR(255),
    IN p_AppointmentDateTime DATETIME
)
BEGIN
    INSERT INTO Appointments (CustomerID, EmployeeID, ServiceType, AppointmentDateTime, Status)
    VALUES (p_CustomerID, p_EmployeeID, p_ServiceType, p_AppointmentDateTime, 'Pending');
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER CheckAppointmentAvailability
BEFORE INSERT ON Appointments
FOR EACH ROW
BEGIN
    DECLARE appointmentCount INT;
    SET appointmentCount = (
        SELECT COUNT(*)
        FROM Appointments
        WHERE EmployeeID = NEW.EmployeeID
        AND DATE(AppointmentDateTime) = DATE(NEW.AppointmentDateTime)
        AND Status = 'Confirmed'
    );
    IF appointmentCount >= 5 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Appointment slot is already booked for this time.';
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE MakeDeposit(
    IN p_AccountID INT,
    IN p_Amount DECIMAL(10, 2)
)
BEGIN
    START TRANSACTION;
    UPDATE Accounts
    SET AccountBalance = AccountBalance + p_Amount
    WHERE AccountID = p_AccountID;
    INSERT INTO Transactions (AccountID, TransactionType, TransactionAmount, TransactionDate)
    VALUES (p_AccountID, 'Deposit', p_Amount, NOW());
    COMMIT;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER EnforceTransactionLimits
BEFORE INSERT ON Transactions
FOR EACH ROW
BEGIN
    DECLARE totalTransactions DECIMAL(10, 2);
    SET totalTransactions = (
        SELECT SUM(TransactionAmount)
        FROM Transactions
        WHERE AccountID = NEW.AccountID
    );
    IF totalTransactions + NEW.TransactionAmount > 1000 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Transaction limit exceeded.';
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE CreateCustomerAccount(
    IN p_FirstName VARCHAR(255),
    IN p_LastName VARCHAR(255),
    IN p_Email VARCHAR(255),
    IN p_Phone VARCHAR(20)
)
BEGIN
    INSERT INTO Customers (FirstName, LastName, Email, Phone)
    VALUES (p_FirstName, p_LastName, p_Email, p_Phone);
    
    -- Create a corresponding account for the customer
    INSERT INTO Accounts (CustomerID, AccountType, AccountBalance, Status)
    VALUES (LAST_INSERT_ID(), 'Savings', 0.0, 'Active');
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER EnforceMaxAppointmentsPerDay
BEFORE INSERT ON Appointments
FOR EACH ROW
BEGIN
    DECLARE appointmentCount INT;
    SET appointmentCount = (
        SELECT COUNT(*)
        FROM Appointments
        WHERE CustomerID = NEW.CustomerID
        AND DATE(AppointmentDateTime) = DATE(NEW.AppointmentDateTime)
        AND Status = 'Confirmed'
    );
    IF appointmentCount >= 3 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Maximum appointments per day exceeded.';
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE ApplyForLoan(
    IN p_CustomerID INT,
    IN p_LoanType VARCHAR(255),
    IN p_LoanAmount DECIMAL(10, 2)
)
BEGIN
    -- Check if the customer is eligible for a loan based on business logic
    IF p_LoanAmount <= 10000 THEN
        INSERT INTO Loans (CustomerID, LoanType, LoanAmount, LoanStatus)
        VALUES (p_CustomerID, p_LoanType, p_LoanAmount, 'Pending');
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Loan amount exceeds the maximum limit.';
    END IF;
END //
DELIMITER ;

--not implemented

-- Procedure to Deposit Money into a Savings Account
DELIMITER //
CREATE PROCEDURE DepositSavingsAccount(
    IN p_AccountID INT,
    IN p_Amount DECIMAL(10, 2)
)
BEGIN
    UPDATE SavingsAccounts
    SET Balance = Balance + p_Amount
    WHERE AccountID = p_AccountID;
    -- You may want to add logic to calculate and credit interest here
END //
DELIMITER ;

-- Trigger to Enforce Draft Limit for Savings Accounts
DELIMITER //
CREATE TRIGGER EnforceDraftLimitSavings
BEFORE INSERT ON Transactions
FOR EACH ROW
BEGIN
    IF NEW.TransactionType = 'Draft' THEN
        DECLARE savingsBalance DECIMAL(10, 2);
        SET savingsBalance = (SELECT Balance FROM SavingsAccounts WHERE AccountID = NEW.AccountID);
        IF NEW.TransactionAmount > savingsBalance THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Insufficient balance for draft.';
        END IF;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE UpdateCustomerPassword(
    IN p_CustomerID INT,
    IN p_NewPassword VARCHAR(255)
)
BEGIN
    UPDATE Customers
    SET Password = p_NewPassword
    WHERE CustomerID = p_CustomerID;
END //
DELIMITER ;



--implemented
DELIMITER //
CREATE PROCEDURE ApplyForLoan(
    IN p_CustomerID INT,
    IN p_LoanAmount DECIMAL(10, 2)
)
BEGIN
    INSERT INTO LoanApplications (CustomerID, LoanAmount) VALUES (p_CustomerID, p_LoanAmount);
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE VerifyLoanApplication(
    IN p_ApplicationID INT,
    IN p_Status ENUM('Approved', 'Rejected'),
    IN p_VerificationNotes TEXT
)
BEGIN
    UPDATE LoanApplications
    SET Status = p_Status, VerificationNotes = p_VerificationNotes
    WHERE ApplicationID = p_ApplicationID;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE ApproveLoanApplication(
    IN p_ApplicationID INT,
    IN p_Status ENUM('Approved', 'Rejected'),
    IN p_AdminNotes TEXT
)
BEGIN
    UPDATE LoanApplications
    SET Status = p_Status, AdminNotes = p_AdminNotes
    WHERE ApplicationID = p_ApplicationID;
END //
DELIMITER ;


# Function to update customer password
def update_customer_password(customer_id, new_password):
    sql = "CALL UpdateCustomerPassword(%s, %s)"
    values = (customer_id, new_password)
    execute_query(sql, values)
    print("Password updated successfully.")

DELIMITER //
CREATE PROCEDURE SetStrongPassword(
    IN p_CustomerID INT,
    IN p_NewPassword VARCHAR(255)
)
BEGIN
    DECLARE uppercase_required TINYINT;
    DECLARE lowercase_required TINYINT;
    DECLARE digit_required TINYINT;
    DECLARE special_required TINYINT;
    
    SET uppercase_required = 1; -- Set to 1 to require at least one uppercase letter
    SET lowercase_required = 1; -- Set to 1 to require at least one lowercase letter
    SET digit_required = 1;     -- Set to 1 to require at least one digit
    SET special_required = 1;   -- Set to 1 to require at least one special character
    
    IF LENGTH(p_NewPassword) < 8 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Password must be at least 8 characters long.';
    ELSEIF uppercase_required = 1 AND NOT REGEXP_LIKE(p_NewPassword, '[A-Z]') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Password must contain at least one uppercase letter.';
    ELSEIF lowercase_required = 1 AND NOT REGEXP_LIKE(p_NewPassword, '[a-z]') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Password must contain at least one lowercase letter.';
    ELSEIF digit_required = 1 AND NOT REGEXP_LIKE(p_NewPassword, '[0-9]') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Password must contain at least one digit.';
    ELSEIF special_required = 1 AND NOT REGEXP_LIKE(p_NewPassword, '[!@#$%^&*()]') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Password must contain at least one special character.';
    ELSE
        UPDATE Customers
        SET Password = p_NewPassword
        WHERE CustomerID = p_CustomerID;
    END IF;
END //
DELIMITER ;

# Function to set a strong password for a customer
def set_strong_password(customer_id, new_password):
    sql = "CALL SetStrongPassword(%s, %s)"
    values = (customer_id, new_password)
    
    try:
        execute_query(sql, values)
        print("Strong password set successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
