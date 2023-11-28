import mysql.connector
import pickle
from mysql.connector import errorcode



# Establish connection
query=""
Password=""
Database=""
def sqlpwd():
    global Password
    cred = open("cred.dat","rb")
    dat=pickle.load(cred)
    cred.close()
    Password=dat[0]
    return Password

def sqldb():
    global Database
    cred = open("cred.dat","rb")
    dat=pickle.load(cred)
    cred.close()
    Database=dat[1]
    return Database

def connectionquery():
    try:
        Databa=sqldb()
        Passwo=sqlpwd()
        query=mysql.connector.connect(host="localhost",user="root",password=Passwo,database=Databa)
    except:
        import traceback
        traceback.print_exc()
        query=""
    return query

# Create the HireEmployee procedure

hire_employee_procedure = """
DELIMITER $$
CREATE PROCEDURE HireEmployee(
    IN emp_no INT,
    IN birth_date DATE,
    IN first_name VARCHAR(50),
    IN last_name VARCHAR(50),
    IN gender ENUM('M', 'F'),
    IN hire_date DATE
)
BEGIN
    INSERT INTO employees (emp_no, birth_date, first_name, last_name, gender, hire_date)
    VALUES (emp_no,birth_date, first_name, last_name, gender, hire_date);
END $$

DELIMITER ;
"""

def hire_employee():
    query=connectionquery()
    cursor=query.cursor()
    # Execute the procedure creation statement
    cursor.execute(hire_employee_procedure, multi=True)

    # Commit the changes
    query.commit()

    # Close connections
    cursor.close()
    query.close()
