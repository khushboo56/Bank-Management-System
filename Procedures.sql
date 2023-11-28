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


DELIMITER //

CREATE PROCEDURE UpdateCashInHand(
    IN cash_in_hand DECIMAL(10, 2),
    IN acc_no INT
)
BEGIN
    UPDATE cash_in_hand SET cash_in_hand = cash_in_hand - cash_in_hand WHERE acc_no = acc_no;
END //

DELIMITER ;

CALL UpdateAccountBalance('savings', 1000.00, 1001);
CALL UpdateCashInHand(500.00, 1001);
CALL UpdateAccountBalance('current', 1500.00, 1003);
CALL UpdateCashInHand(800.00, 1003);


DELIMITER //

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

CALL WithdrawMoney(1001, 'S', 3000.00);
CALL WithdrawMoney(1001, 'S', 5000.00);
CALL WithdrawMoney(1003, 'C', 8000.00);


DELIMITER //

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

#TESTREDEEMCODE IS THE REEDEMCODE USE IN THE PYTHON CODE

CALL RedeemCode('TESTREDEEMCODE', 'savings', 1002); //VALID
CALL RedeemCode('INVALIDCODE', 'current', 1003);
CALL RedeemCode('ANOTHERCODE', 'savings', 1004);







