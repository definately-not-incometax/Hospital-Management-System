-- ============================================================
-- Hospital Management System — Database Schema
-- Author: Bhaskarjyoti Dey
-- Engine: MySQL / MariaDB
-- Description: Normalised relational schema (3NF) covering
--              patients, doctors, appointments, admissions,
--              billing, and prescriptions.
-- ============================================================

CREATE DATABASE IF NOT EXISTS hospital_db;
USE hospital_db;

-- ------------------------------------------------------------
-- 1. Departments
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS departments (
    department_id   INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL UNIQUE,
    location        VARCHAR(100)
);

-- ------------------------------------------------------------
-- 2. Doctors
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id       INT AUTO_INCREMENT PRIMARY KEY,
    first_name      VARCHAR(50) NOT NULL,
    last_name       VARCHAR(50) NOT NULL,
    specialization  VARCHAR(100),
    phone           VARCHAR(15),
    email           VARCHAR(100) UNIQUE,
    department_id   INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- ------------------------------------------------------------
-- 3. Patients
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS patients (
    patient_id      INT AUTO_INCREMENT PRIMARY KEY,
    first_name      VARCHAR(50) NOT NULL,
    last_name       VARCHAR(50) NOT NULL,
    date_of_birth   DATE,
    gender          ENUM('Male', 'Female', 'Other') NOT NULL,
    phone           VARCHAR(15),
    email           VARCHAR(100),
    address         VARCHAR(255),
    blood_group     VARCHAR(5),
    registered_on   DATE DEFAULT (CURRENT_DATE)
);

-- ------------------------------------------------------------
-- 4. Appointments
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id   INT AUTO_INCREMENT PRIMARY KEY,
    patient_id       INT NOT NULL,
    doctor_id        INT NOT NULL,
    appointment_date DATETIME NOT NULL,
    reason           VARCHAR(255),
    status           ENUM('Scheduled', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ------------------------------------------------------------
-- 5. Admissions (in-patient tracking)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS admissions (
    admission_id    INT AUTO_INCREMENT PRIMARY KEY,
    patient_id      INT NOT NULL,
    doctor_id       INT NOT NULL,
    room_number     VARCHAR(10),
    admit_date      DATE NOT NULL,
    discharge_date  DATE,
    diagnosis       VARCHAR(255),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ------------------------------------------------------------
-- 6. Prescriptions
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS prescriptions (
    prescription_id  INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id   INT NOT NULL,
    medicine_name    VARCHAR(150) NOT NULL,
    dosage           VARCHAR(50),
    duration_days    INT,
    notes            VARCHAR(255),
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);
-- ------------------------------------------------------------
-- 7. Billing
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS billing (
    bill_id         INT AUTO_INCREMENT PRIMARY KEY,
    patient_id      INT NOT NULL,
    appointment_id  INT,
    admission_id    INT,
    amount          DECIMAL(10, 2) NOT NULL,
    bill_date       DATE DEFAULT (CURRENT_DATE),
    payment_status  ENUM('Paid', 'Pending', 'Cancelled') DEFAULT 'Pending',
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (admission_id) REFERENCES admissions(admission_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- ------------------------------------------------------------
-- 8. Staff (nurses, receptionists, admin)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS staff (
    staff_id        INT AUTO_INCREMENT PRIMARY KEY,
    first_name      VARCHAR(50) NOT NULL,
    last_name       VARCHAR(50) NOT NULL,
    role            VARCHAR(50),
    phone           VARCHAR(15),
    department_id   INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- ------------------------------------------------------------
-- 9. Medicines (inventory reference table)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS medicines (
    medicine_id     INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(150) NOT NULL UNIQUE,
    manufacturer    VARCHAR(150),
    unit_price      DECIMAL(8, 2),
    stock_quantity  INT DEFAULT 0
);

-- ------------------------------------------------------------
-- 10. Users (login accounts for the GUI application)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id         INT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    role            ENUM('Admin', 'Receptionist', 'Doctor') DEFAULT 'Receptionist',
    created_on      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Indexes for common lookups
-- ------------------------------------------------------------
CREATE INDEX idx_patient_name ON patients(last_name, first_name);
CREATE INDEX idx_doctor_specialization ON doctors(specialization);
CREATE INDEX idx_appointment_date ON appointments(appointment_date);
CREATE INDEX idx_billing_status ON billing(payment_status);

