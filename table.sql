TABLES['employees'] = (
    "CREATE TABLE IF NOT EXISTS `employees` ("
    "  `emp_no` int(5) NOT NULL ,"
    "  `birth_date` date NOT NULL,"
    "  `first_name` varchar(15) NOT NULL,"
    "  `last_name` varchar(15) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `hire_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
    ") ")

TABLES['clients'] = (
    "CREATE TABLE IF NOT EXISTS`clients` ("
    "  `acc_no` int NOT NULL PRIMARY KEY,"
    "  `type` enum('S','C') NOT NULL,"
    "  `first_name` varchar(15) NOT NULL,"
    "  `last_name` varchar(15) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `birth_date` date NOT NULL,"
    "  `accd` date NOT NULL,"
    "  `mobile_no` varchar(20) NOT NULL,"
    "  `email_id` varchar(25) NOT NULL,"
    "  `pass` varchar(8) NOT NULL"
    ") "
)

TABLES['empass'] = (
    "CREATE TABLE IF NOT EXISTS `empass` ("
    "  `emp_no` int(5) NOT NULL,"
    "  `pass` varchar(8) NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
    ") "
)


TABLES['savings'] = (
    "CREATE TABLE IF NOT EXISTS `savings` ("
    "  `acc_no` int(5) NOT NULL,"
    "  `balance` int NOT NULL,"
    "  `loan` enum('YES','NO') NOT NULL,"
    "  PRIMARY KEY (`acc_no`)"
    ") "
)

TABLES['current'] = (
    "CREATE TABLE IF NOT EXISTS `current` ("
    "  `acc_no` int(5) NOT NULL,"
    "  `balance` int NOT NULL,"
    "  `overdraft` enum('YES','NO') NOT NULL,"
    "  PRIMARY KEY (`acc_no`)"
    ") "
)

TABLES['loan'] = (
    "CREATE TABLE IF NOT EXISTS `loan` ("
    "  `acc_no` int(5) NOT NULL,"
    "  `loan_type` enum('PL','HL','EL','TL','BL') NOT NULL,"
    "  `loan_amt` int NOT NULL,"
    "  `time_period_months` int NOT NULL,"
    "  `iterest_perc_per_annum` int(1) NOT NULL,"
    "  `amt-per-month` int NOT NULL,"
    "  `remaining_amt` int NOT NULL,"
    "  PRIMARY KEY (`acc_no`)"
    ") "
)

TABLES['overdraft']=(
    "CREATE TABLE IF NOT EXISTS `overdraft` ("
    "  `acc_no` int(5) NOT NULL,"
    "  `overdraft_amt` int NOT NULL,"
    "  `od_with_interest_remaining` int NOT NULL,"
    "  PRIMARY KEY (`acc_no`)"
    ") "
)

TABLES['cash_in_hand']=(
    "CREATE TABLE IF NOT EXISTS`cash_in_hand` ("
    "  `acc_no` int(5) NOT NULL,"
    "  `cash_in_hand` int NOT NULL,"
    "  PRIMARY KEY (`acc_no`)"
    ") "
)