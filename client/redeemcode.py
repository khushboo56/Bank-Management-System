from tools import dataentering
def cp4(conn,cur,acc_type,acc_no):
    rc=input("Enter redeem code: ")
    if rc=="TESTREDEEMCODE":
        query="update {} set balance = balance+%s where acc_no = %s".format(acc_type)
        data=(5000,acc_no)
        done = dataentering.tableupdate(conn,cur,query,data)
        if done:
            print("Added 5000 currency to your account!!")
        else:
            print("There was a problem while processing the request")
    else:
        print("Sorry! This redeem code doesn't work")
"""
import mysql.connector
from tools import dataentering

# Establish connection
connection = mysql.connector.connect(
    host="your_host",
    user="your_username",
    password="your_password",
    database="your_database"
)

# Create a cursor object using the connection
cursor = connection.cursor()

# Create the RedeemCode procedure
redeem_code_procedure = 

DELIMITER //"""
""""
CREATE PROCEDURE RedeemCode(
    IN rc VARCHAR(50),
    IN acc_type VARCHAR(50),
    IN acc_no INT
)
BEGIN
    DECLARE redeem_amount INT DEFAULT 5000;
    
    IF rc = 'TESTREDEEMCODE' THEN
        UPDATE {acc_type} SET balance = balance + redeem_amount WHERE acc_no = acc_no;
    END IF;

END //

DELIMITER ;
"""
"""
# Execute the procedure creation statement
cursor.execute(redeem_code_procedure, multi=True)

# Commit the changes
connection.commit()

# Function to redeem code
def redeem_code(conn, cur, acc_type, acc_no):
    rc = input("Enter redeem code: ")

    try:
        # Call the RedeemCode procedure
        cursor.callproc('RedeemCode', (rc, acc_type, acc_no))
        connection.commit()

        # Check if the redeem code was valid and processed
        cursor.execute(f"SELECT ROW_COUNT() AS rows_updated")
        rows = cursor.fetchone()
        if rows and rows[0] > 0:
            print("Added 5000 currency to your account!!")
        else:
            print("Sorry! This redeem code doesn't work")

    except mysql.connector.Error as err:
        print(err.msg)
        print("There was a problem while processing the request")

# Call the redeem_code function
try:
    acc_type = "your_account_type"  # Replace with the actual account type
    acc_no = 123  # Replace with the actual account number
    redeem_code(connection, cursor, acc_type, acc_no)

except mysql.connector.Error as err:
    print(err.msg)

finally:
    # Close connections
    cursor.close()
    connection.close()"""
