from tools import dataentering
def cp2(conn,cur,acc_type,acc_no):
    cash_in_hand=dataentering.handcash(conn,cur,acc_no)
    
    deposit_amt=dataentering.amounts("deposit",cash_in_hand,acc_type)
    deposit_amt=deposit_amt[0]
    # Execute the procedure creation statements
   # cur.execute(update_balance_procedure, multi=True)
   # cur.execute(UpdateCashInHand, multi=True)
   # conn.commit()
    if deposit_amt:
        if acc_type == "savings":
            query2 = "CALL UpdateSavingsBalance(%s, %s)"
        elif acc_type == "current":
            query2 = "CALL UpdateCurrentBalance(%s, %s)"
        else:
            print("Invalid account type")
            return
       # query2="update {} set balance = balance+%s where acc_no = %s".format(acc_type)
        #query2= ("CALL UpdateAccountBalance({})(%s,%s)".format(acc_type))  #facing problem in running of Update Account Balance due to acc_type
        data2=(deposit_amt,acc_no)
        done2=dataentering.tableupdate(conn,cur,query2,data2)
        if done2:
            #query3="update cash_in_hand set cash_in_hand = cash_in_hand-%s where acc_no = %s"
            query3 = ("CALL UpdateCashInHand(%s,%s)")
            data3=(cash_in_hand,acc_no)
            done3=dataentering.tableupdate(conn,cur,query3,data3)
            if done3:
                print("Deposit of {} currency successful".format(deposit_amt))
                print()
            else:
                query2="update {} set balance = balance-%s where acc_no = %s".format(acc_type)
                data2=(deposit_amt,acc_no)
                done2=dataentering.tableupdate(conn,cur,query2,data2)
                if done2:
                    print("Unable to subtract amount from cash_in_hand\n")
        else:
            print("Error while trying to add amount to balance.\n")
    else: 
        pass 


    """

import mysql.connector

# Establish connection


# Create a cursor object using the connection
cursor = connection.cursor()

# Create the UpdateAccountBalance procedure
update_account_balance_procedure = 
DELIMITER //

CREATE PROCEDURE UpdateAccountBalance(
    IN acc_type VARCHAR(50),
    IN deposit_amt DECIMAL(10, 2),
    IN acc_no INT
)
BEGIN
    UPDATE {acc_type} SET balance = balance + deposit_amt WHERE acc_no = acc_no;
END //

DELIMITER ;


# Create the UpdateCashInHand procedure
update_cash_in_hand_procedure = 
DELIMITER //

CREATE PROCEDURE UpdateCashInHand(
    IN cash_in_hand DECIMAL(10, 2),
    IN acc_no INT
)
BEGIN
    UPDATE cash_in_hand SET cash_in_hand = cash_in_hand - cash_in_hand WHERE acc_no = acc_no;
END //

DELIMITER ;


# Execute the procedure creation statements
cursor.execute(update_account_balance_procedure, multi=True)
cursor.execute(update_cash_in_hand_procedure, multi=True)

# Commit the changes
connection.commit()

# Function to deposit amount
def deposit_amount(conn, cur, acc_type, acc_no):
    cash_in_hand = dataentering.handcash(conn, cur, acc_no)
    deposit_amt = dataentering.amounts("deposit", cash_in_hand, acc_type)[0]

    if deposit_amt:
        try:
            # Call the UpdateAccountBalance procedure
            cursor.callproc('UpdateAccountBalance', (acc_type, deposit_amt, acc_no))
            connection.commit()

            # Call the UpdateCashInHand procedure
            cursor.callproc('UpdateCashInHand', (cash_in_hand, acc_no))
            connection.commit()

            print("Deposit of {} currency successful".format(deposit_amt))
            print()

        except mysql.connector.Error as err:
            print(err.msg)
            print("Error while trying to update account balance or cash in hand.\n")

    else:
        print("Deposit amount is zero.\n")

"""