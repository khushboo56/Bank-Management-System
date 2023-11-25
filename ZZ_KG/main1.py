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

# Function to execute SELECT queries
def execute_select_query(sql, values=None):
    cursor = db.cursor()
    cursor.execute(sql, values)
    result = cursor.fetchall()
    return result

def is_username_available(role, username):
    if role == "admin":
        sql = "SELECT COUNT(*) FROM admins WHERE Username = %s"
    elif role == "employee":
        sql = "SELECT COUNT(*) FROM bankemployees WHERE Username = %s"
    elif role == "customer":
        sql = "SELECT COUNT(*) FROM customers WHERE Username = %s"
    else:
        return False

    values = (username,)
    result = execute_select_query(sql, values)

    return result[0][0] == 0

# Function to sign up a new user
def sign_up(role, username, password, **additional_info):
    if is_username_available(role, username):
        if role == "admin":
            sql = "INSERT INTO admins (Username, Password, FirstName, LastName) VALUES (%s, %s, %s, %s)"
            values = (username, password, additional_info.get("first_name", ""), additional_info.get("last_name", ""))
        elif role == "employee":
            sql = "INSERT INTO bankemployees (Username, Password, FirstName, LastName, Department) VALUES (%s, %s, %s, %s, %s)"
            values = (username, password, additional_info.get("first_name", ""), additional_info.get("last_name", ""), additional_info.get("department", ""))
        elif role == "customer":
            sql = "INSERT INTO customers (Username, Password, FirstName, LastName, DateOfBirth, ContactInformation, Address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (username, password, additional_info.get("first_name", ""), additional_info.get("last_name", ""), additional_info.get("dob", ""), additional_info.get("contact_info", ""), additional_info.get("address", ""))
        else:
            return False

        execute_query(sql, values)
        print(f"{role.capitalize()} registration successful.")
        return True
    else:
        print("Username is already taken. Please choose another.")
        return False


# Admin sign up
def admin_sign_up():
    print("\nAdmin Sign Up")
    username = input("Username: ")
    password = input("Password: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    sign_up("admin", username, password, first_name=first_name, last_name=last_name)

# Employee sign up
def employee_sign_up():
    print("\nEmployee Sign Up")
    username = input("Username: ")
    password = input("Password: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    department = input("Department: ")
    sign_up("employee", username, password, first_name=first_name, last_name=last_name, department=department)

def customer_sign_up():
    print("\nCustomer Sign Up")
    username = input("Username: ")
    password = input("Password: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    dob = input("Date of Birth (YYYY-MM-DD): ")
    contact_info = input("Contact Information: ")
    address = input("Address: ")
    sign_up("customer", username, password, first_name=first_name, last_name=last_name, dob=dob, contact_info=contact_info, address=address)









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

# Function to apply for a loan (Client)
def apply_for_loan(customer_id, loan_amount):
    sql = "CALL ApplyForLoan(%s, %s)"
    values = (customer_id, loan_amount)
    execute_query(sql, values)
    print("Loan application submitted. Please wait for verification and approval.")

# Function to verify a loan application (Employee)
def verify_loan_application(application_id, status, verification_notes):
    sql = "CALL VerifyLoanApplication(%s, %s, %s)"
    values = (application_id, status, verification_notes)
    execute_query(sql, values)
    print("Loan application verified.")

# Function to approve or reject a loan application (Admin)
def approve_loan_application(application_id, status, admin_notes):
    sql = "CALL ApproveLoanApplication(%s, %s, %s)"
    values = (application_id, status, admin_notes)
    execute_query(sql, values)
    print("Loan application decision made.")



# Function to check login credentials
def login(role, username, password):
    if role == "admin":
        sql = "SELECT AdminID FROM admins WHERE Username = %s AND Password = %s"
    elif role == "employee":
        sql = "SELECT EmployeeID FROM bankemployees WHERE Username = %s AND Password = %s"
    elif role == "customer":
        sql = "SELECT CustomerID FROM customers WHERE Username = %s AND Password = %s"
    else:
        return None

    values = (username, password)
    result = execute_select_query(sql, values)

    if result:
        return result[0][0]
    else:
        return None

# Admin login
def admin_login():
    print("\nAdmin Login")
    username = input("Username: ")
    password = input("Password: ")
    admin_id = login("admin", username, password)
    if admin_id:
        print("Admin login successful. Admin ID:", admin_id)
        # Add admin-specific functionalities here
    else:
        print("Invalid credentials. Login failed.")

# Employee login
def employee_login():
    print("\nEmployee Login")
    username = input("Username: ")
    password = input("Password: ")
    employee_id = login("employee", username, password)
    if employee_id:
        print("Employee login successful. Employee ID:", employee_id)
        # Add employee-specific functionalities here
    else:
        print("Invalid credentials. Login failed.")

# Customer login
def customer_login():
    print("\nCustomer Login")
    username = input("Username: ")
    password = input("Password: ")
    customer_id = login("customer", username, password)
    if customer_id:
        print("Customer login successful. Customer ID:", customer_id)
        # Add customer-specific functionalities here
    else:
        print("Invalid credentials. Login failed.")



# Main menu
while True:
    print("\nBanking Reservation System")
    
    print("1. Admin Login")
    print("2. Employee Login")
    print("3. Customer Login")
    print("4. Admin Sign Up")
    print("5. Employee Sign Up")
    print("6. Customer Sign Up")
    print("7. Schedule Appointment")
    print("8. Confirm Appointment")
    print("9. Apply for Loan")
    print("10. Verify Loan Application (Employee)")
    print("11. Approve/Reject Loan Application (Admin)")
    print("12. Exit")
    
    choice = input("Enter your choice: ")
    if choice == '1':
        admin_login()
    elif choice == '2':
        employee_login()
    elif choice == '3':
        customer_login()
    elif choice == '4':
        admin_sign_up()
    elif choice == '5':
        employee_sign_up()
    elif choice == '6':
        customer_sign_up()
    elif choice == '7':
        customer_id = input("Customer ID: ")
        employee_id = input("Employee ID: ")
        service_type = input("Service Type: ")
        appointment_datetime = input("Appointment Date and Time (YYYY-MM-DD HH:MM:SS): ")
        schedule_appointment(customer_id, employee_id, service_type, appointment_datetime)
    elif choice == '8':
        appointment_id = input("Appointment ID: ")
        confirm_appointment(appointment_id)
    elif choice == '9':
        customer_id = int(input("Customer ID: "))
        loan_amount = float(input("Loan Amount: "))
        apply_for_loan(customer_id, loan_amount)
    
    elif choice == '10':
        employee_id = int(input("Employee ID: "))
        application_id = int(input("Loan Application ID: "))
        status = input("Status (Approved/Rejected): ")
        verification_notes = input("Verification Notes: ")
        verify_loan_application(application_id, status, verification_notes)
    
    elif choice == '11':
        admin_id = int(input("Admin ID: "))
        application_id = int(input("Loan Application ID: "))
        status = input("Status (Approved/Rejected): ")
        admin_notes = input("Admin Notes: ")
        approve_loan_application(application_id, status, admin_notes)
    elif choice == '12':
        break
