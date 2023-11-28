from tools import dataentering
def cp6(conn,cur,acc_type,acc_no,balance):
    acc_to_transfer=dataentering.primary_key_no("acc_no of receiver")
    cur.execute("select * from clients where acc_no={}".format(acc_to_transfer))
    result=cur.fetchall()
    if result==[]:
        print("That account number doesn't exist\n")
    elif acc_to_transfer==acc_no:
        print("You can't transfer to yourself\n")
    else:
        acc_type_receiver=result[0][1]
        if acc_type_receiver == 'S': acc_type_receiver="savings"
        if acc_type_receiver == 'C': acc_type_receiver="current"
        fname,lname=result[0][2],result[0][3]
        transfer_amt,overdraft=dataentering.amounts("transfer",balance,acc_type)
        print(" Y - Yes")
        print(" N - No")
        ch=input("Do you want transfer {} currency to {} {}'s account: ".format(transfer_amt,fname,lname))
        if ch == "Y" :

            if transfer_amt:
                if acc_type=="current":
                    if overdraft!=None:
                        print('''You will be notified about the overdraft status when an employee
                                sanctions your overdraft...''')
                        #TODO:some more stuff 
                else:
                    query="update {} set balance=balance-%s where acc_no = %s".format(acc_type)
                    data=(transfer_amt,acc_no)
                    done=dataentering.tableupdate(conn,cur,query,data)
                    if done:
                        query2="update {} set balance=balance+%s where acc_no=%s".format(acc_type_receiver)
                        data2=(transfer_amt,acc_to_transfer)
                        done2=dataentering.tableupdate(conn,cur,query2,data2)
                        if done2:
                            print("Successfully transferred {} currency\n".format(transfer_amt))
                        else:
                            query="update {} set balance=balance+%s where acc_no = %s".format(acc_type)
                            data=(transfer_amt,acc_no)
                            done=dataentering.tableupdate(conn,cur,query,data)
                            if done:
                                print("Couldn't update receiver's balance\n")
                    else:
                        print("Couldn't transfer money.")
            else :
                print("You do not have enough balance!!")

        else:
            print("Cancelled transfer")

""" import mysql.connector
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

# Create the TransferMoney procedure
transfer_money_procedure = """
"""
DELIMITER //

CREATE PROCEDURE TransferMoney(
    IN acc_no_sender INT,
    IN acc_no_receiver INT,
    IN balance DECIMAL(10, 2)
)
BEGIN
    DECLARE transfer_amt DECIMAL(10, 2);
    DECLARE overdraft DECIMAL(10, 2);
    DECLARE acc_type_sender VARCHAR(50);
    DECLARE acc_type_receiver VARCHAR(50);
    DECLARE fname VARCHAR(50);
    DECLARE lname VARCHAR(50);

    SELECT acc_type INTO acc_type_sender FROM clients WHERE acc_no = acc_no_sender;
    SELECT acc_type INTO acc_type_receiver, first_name, last_name FROM clients WHERE acc_no = acc_no_receiver;

    IF acc_type_receiver = 'S' THEN
        SET acc_type_receiver = 'savings';
    ELSEIF acc_type_receiver = 'C' THEN
        SET acc_type_receiver = 'current';
    END IF;

    SELECT balance INTO transfer_amt, overdraft FROM your_table WHERE conditions;  -- Fetch transfer_amt and overdraft

    -- Proceed with the transfer logic as needed based on your requirements

END //

DELIMITER ;
"""
"""
# Execute the procedure creation statement
cursor.execute(transfer_money_procedure, multi=True)

# Commit the changes
connection.commit()

# Function to transfer money
def transfer_money(conn, cur, acc_no_sender, acc_no_receiver, balance):
    # Call the TransferMoney procedure
    try:
        cursor.callproc('TransferMoney', (acc_no_sender, acc_no_receiver, balance))
        connection.commit()
        print("Successfully transferred currency\n")

    except mysql.connector.Error as err:
        print(err.msg)
        print("Error occurred during the transfer process.")

# Call the transfer_money function
try:
    acc_no_sender = 123  # Replace with the actual sender's account number
    acc_no_receiver = 456  # Replace with the actual receiver's account number
    balance = 1000  # Replace with the actual balance to transfer

    transfer_money(connection, cursor, acc_no_sender, acc_no_receiver, balance)

except mysql.connector.Error as err:
    print(err.msg)

finally:
    # Close connections
    cursor.close()
    connection.close()
"""