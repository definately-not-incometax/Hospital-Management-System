# Hospital Management System

A desktop Hospital Management System built with Python (Tkinter) and MySQL/MariaDB, providing CRUD operations for patients, doctors, appointments, and billing through a normalised relational database.

## Features

- Patient management — add, search, update, and delete patient records
- Doctor directory — view doctors with their department and specialization
- Appointment scheduling — book appointments and mark them completed
- Billing — track charges per patient/appointment and mark bills as paid
- Authentication — SHA-256 hashed user login (Admin / Receptionist / Doctor roles)
- 10-table normalised (3NF) schema: patients, doctors, departments, appointments, admissions, prescriptions, billing, staff, medicines, users

## Tech Stack

| Layer      | Technology              |
|------------|--------------------------|
| GUI        | Python 3, Tkinter/ttk    |
| Database   | MySQL / MariaDB          |
| DB Driver  | mysql-connector-python   |
| Testing    | unittest                 |

## Project Structure

hospital-management-system/
- database/
  - schema.sql (Table definitions - 3NF, FKs, indexes)
  - seed_data.sql (Sample demo data)
  - db_connector.py (Database access layer - CRUD helpers)
- gui/
  - main.py (Tkinter application - 4 tabs)
- tests/
  - test_db_connector.py (Automated tests - 11 cases, all passing)
- requirements.txt
- README.md

## Setup

### 1. Install MySQL/MariaDB and create the database

Run in terminal:
sudo apt install mariadb-server
sudo service mariadb start
mysql -u root < database/schema.sql
mysql -u root < database/seed_data.sql

Create the app's DB user:
CREATE USER 'hms_user'@'localhost' IDENTIFIED BY 'hms_pass123';
GRANT ALL PRIVILEGES ON hospital_db.* TO 'hms_user'@'localhost';
FLUSH PRIVILEGES;

### 2. Install Python dependencies

pip install -r requirements.txt

### 3. Run the application

cd gui
python main.py

## Running Tests

python -m unittest tests.test_db_connector -v

Expected output: 11 tests, all passing.

## Database Schema Overview

- patients — demographic and contact info
- doctors — linked to departments
- appointments — links patients to doctors with date/status
- admissions — in-patient room/diagnosis tracking
- prescriptions — linked to appointments
- billing — linked to patients/appointments/admissions
- staff, medicines, users — supporting tables

All foreign keys use ON DELETE/ON UPDATE cascades appropriate to each relationship.

## Author

Bhaskarjyoti Dey
