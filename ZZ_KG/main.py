import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Kgupta@8646",
    database="bank_reservation"
)

# Function to execute SQL queries
def execute_query(sql, values=None):
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()

# Create tables for Bank Employees, Accounts, Transactions, and Loans
execute_query("""
CREATE TABLE IF NOT EXISTS BankEmployees (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Department VARCHAR(255)
)
""")
execute_query("""
CREATE TABLE IF NOT EXISTS Accounts (
    AccountID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    AccountType VARCHAR(255),
    AccountBalance DECIMAL(10, 2),
    Status VARCHAR(20),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
)
""")
execute_query("""
CREATE TABLE IF NOT EXISTS Transactions (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    AccountID INT,
    TransactionType VARCHAR(255),
    TransactionAmount DECIMAL(10, 2),
    TransactionDate DATETIME,
    FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
)
""")
execute_query("""
CREATE TABLE IF NOT EXISTS Loans (
    LoanID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    LoanType VARCHAR(255),
    LoanAmount DECIMAL(10, 2),
    LoanStatus VARCHAR(20),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
)
""")




# Customer registration
def register_customer(first_name, last_name, dob, contact_info, address):
    sql = "INSERT INTO Customers (FirstName, LastName, DateOfBirth, ContactInformation, Address) VALUES (%s, %s, %s, %s, %s)"
    values = (first_name, last_name, dob, contact_info, address)
    execute_query(sql, values)
    print("Customer registered successfully.")

# Schedule an appointment
def schedule_appointment(customer_id, employee_id, service_type, appointment_datetime):
    sql = "CALL CreateAppointment(%s, %s, %s, %s)"
    values = (customer_id, employee_id, service_type, appointment_datetime)
    try:
        execute_query(sql, values)
        print("Appointment scheduled successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Confirm an appointment
def confirm_appointment(appointment_id):
    sql = "CALL ConfirmAppointment(%s)"
    values = (appointment_id,)
    try:
        execute_query(sql, values)
        print("Appointment confirmed.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Main menu
while True:
    print("\nBanking Reservation System")
    print("1. Register Customer")
    print("2. Schedule Appointment")
    print("3. Confirm Appointment")
    print("4. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == '1':
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        dob = input("Date of Birth (YYYY-MM-DD): ")
        contact_info = input("Contact Information: ")
        address = input("Address: ")
        register_customer(first_name, last_name, dob, contact_info, address)
    elif choice == '2':
        customer_id = input("Customer ID: ")
        employee_id = input("Employee ID: ")
        service_type = input("Service Type: ")
        appointment_datetime = input("Appointment Date and Time (YYYY-MM-DD HH:MM:SS): ")
        schedule_appointment(customer_id, employee_id, service_type, appointment_datetime)
    elif choice == '3':
        appointment_id = input("Appointment ID: ")
        confirm_appointment(appointment_id)
    elif choice == '4':
        break
