-- INSERT statements for 'employees' table
INSERT INTO employees (emp_no, birth_date, first_name, last_name, gender, hire_date)
VALUES (1, '1990-01-01', 'Nikhil', 'Garg', 'M', '2023-01-01');

-- INSERT statements for 'clients' table
INSERT INTO clients (acc_no, type, first_name, last_name, gender, birth_date, accd, mobile_no, email_id, pass)
VALUES (1001, 'S', 'Khushboo', 'Gupta', 'F', '1985-05-10', '2023-01-01', '1234567890', 'khushboo@example.com', '123');

INSERT INTO clients (acc_no, type, first_name, last_name, gender, birth_date, accd, mobile_no, email_id, pass)
VALUES (1003, 'C', 'Priyanshu', 'Kumar', 'M', '1990-05-10', '2023-01-01', '1234567560', 'priyanshu@example.com', '123');


-- INSERT statements for 'empass' table
INSERT INTO empass (emp_no, pass)
VALUES (1, '123');

-- INSERT statements for 'savings' table
INSERT INTO savings (acc_no, balance, loan)
VALUES (1001, 5000, 'NO');

-- INSERT statements for 'current' table
INSERT INTO current (acc_no, balance, overdraft)
VALUES (1003, 10000, 'YES');

-- INSERT statements for 'loan' table
INSERT INTO loan (acc_no, loan_type, loan_amt, time_period_months, iterest_perc_per_annum, amt_per_month, remaining_amt)
VALUES (1001, 'PL', 20000, 12, 5, 1800, 15000);

-- INSERT statements for 'overdraft' table
INSERT INTO overdraft (acc_no, overdraft_amt, od_with_interest_remaining)
VALUES (1003, 5000, 4000);

-- INSERT statements for 'cash_in_hand' table
INSERT INTO cash_in_hand (acc_no, cash_in_hand)
VALUES (1001, 2000);
