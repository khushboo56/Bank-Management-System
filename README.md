# Bank Management System Database Management System (DBMS) Project

## Introduction

This project is a comprehensive Database Management System (DBMS) for a Bank Management System implemented using Python for the application logic and MySQL for the relational database. The system is designed to efficiently manage and organize data related to a bank, catering to three main user roles: Admin, Client, and Employee.

## Features

### Admin Panel
- **User Management:** Admins can add, modify, or remove users, including clients and employees.
- **Access Control:** Admins have the authority to grant or revoke access permissions for employees and clients.

### Client Panel
- **Account Management:** Clients can create new accounts, view account details, and perform transactions.
- **Transaction History:** Clients can access and review their transaction history.
- **Profile Management:** Clients can update their personal information and change login credentials.

### Employee Panel
- **Account Verification:** Employees can verify and approve new account requests from clients.
- **Transaction Processing:** Employees can process various transactions such as deposits, withdrawals, and fund transfers.
- **Customer Support:** Employees have access to client information for providing assistance and support.

### Database Procedures and Triggers
- **Procedures:** Custom procedures are implemented to handle specific tasks efficiently, such as generating account statements or processing transactions.
- **Triggers:** Triggers are set up to automate actions based on specific events in the database, ensuring data consistency and integrity.

## Technology Used

- **Python:** The project's application logic is implemented in Python, offering a versatile and readable codebase.
- **MySQL:** The relational database management system used to store and manage the bank's data efficiently.
