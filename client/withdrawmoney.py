from tools import dataentering
def cp3(conn,cur,acc_type,acc_no):
    cur.execute("select balance from {} where acc_no={}".format(acc_type,acc_no))
    balance=cur.fetchall()
    balance=balance[0][0]
    withdraw_amt=dataentering.amounts("withdraw",balance,acc_type)
    withdraw_amt=withdraw_amt[0]
    if withdraw_amt:
        query="update {} set balance = balance-%s where acc_no=%s".format(acc_type)
        data=(withdraw_amt,acc_no)
        done=dataentering.tableupdate(conn,cur,query,data)
        if done:
            query2="update cash_in_hand set cash_in_hand=cash_in_hand+%s where acc_no=%s"
            data2=(withdraw_amt,acc_no)
            done2=dataentering.tableupdate(conn,cur,query2,data2)
            if done2:
                print("Successfully withdrawn {} currency".format(withdraw_amt))
                print()
            else:
                query="update {} set balance = balance+%s where acc_no=%s".format(acc_type)
                data=(withdraw_amt,acc_no)
                done=dataentering.tableupdate(conn,cur,query,data)
                if done:
                    print("Couldn't remove money from cash_in_hand\n")
        else:
            print("couldn't update balance\n")
    else:
        print("Couldn't withdraw amount\n")


""" DELIMITER //

CREATE PROCEDURE WithdrawMoney(
    IN acc_no INT,
    IN acc_type VARCHAR(50),
    IN balance DECIMAL(10, 2)
)
BEGIN
    DECLARE withdraw_amt DECIMAL(10, 2);

    -- Get withdrawal amount
    SELECT amounts("withdraw", balance, acc_type) INTO withdraw_amt;

    IF withdraw_amt > 0 THEN
        -- Update account balance
        UPDATE clients
        SET balance = balance - withdraw_amt
        WHERE acc_no = acc_no;

        -- Update cash in hand
        UPDATE cash_in_hand
        SET cash_in_hand = cash_in_hand + withdraw_amt
        WHERE acc_no = acc_no;

        SELECT "Successfully withdrawn", withdraw_amt, "currency" AS message;

    ELSE
        SELECT "Couldn't withdraw amount" AS message;
    END IF;

END //

DELIMITER ;

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

# Function to withdraw money using stored procedure
def withdraw_money(conn, cur, acc_no, acc_type):
    try:
        # Get account balance
        cur.execute(f"SELECT balance FROM {acc_type} WHERE acc_no={acc_no}")
        result = cur.fetchall()
        balance = result[0][0]

        # Call the WithdrawMoney procedure
        cur.callproc('WithdrawMoney', (acc_no, acc_type, balance))
        result = cur.fetchone()

        print(result[0], result[1], result[2])

        conn.commit()

    except mysql.connector.Error as err:
        print(err.msg)
        print("Error occurred during the withdrawal process.")

# Call the withdraw_money function
try:
    acc_no = 123  # Replace with the actual account number
    acc_type = "your_account_type"  # Replace with the actual account type

    withdraw_money(connection, cursor, acc_no, acc_type)

except mysql.connector.Error as err:
    print(err.msg)

finally:
    # Close connections
    cursor.close()
    connection.close()

"""