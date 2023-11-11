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

