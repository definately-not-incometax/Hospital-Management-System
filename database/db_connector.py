"""
db_connector.py
================
Central database access layer for the Hospital Management System.

Wraps mysql-connector-python with simple, reusable CRUD helpers
so the GUI layer never writes raw SQL directly.

Author: Bhaskarjyoti Dey
"""

import hashlib
import mysql.connector
from mysql.connector import Error


class Database:
    """Thin wrapper around a MySQL/MariaDB connection with CRUD helpers."""

    def __init__(self, host="localhost", user="hms_user",
                 password=*** database="hospital_db"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=***
                database=self.database,
            )
        except Error as e:
            raise ConnectionError(f"Could not connect to database: {e}")

    def _cursor(self, dictionary=True):
        if self.conn is None or not self.conn.is_connected():
            self.connect()
        return self.conn.cursor(dictionary=dictionary)

    # ------------------------------------------------------------
    # Generic helpers
    # ------------------------------------------------------------
    def execute(self, query, params=None, commit=False):
        """Run an INSERT/UPDATE/DELETE query. Returns lastrowid."""
        cur = self._cursor(dictionary=False)
        cur.execute(query, params or ())
        if commit:
            self.conn.commit()
        last_id = cur.lastrowid
        cur.close()
        return last_id

    def fetch_all(self, query, params=None):
        cur = self._cursor(dictionary=True)
        cur.execute(query, params or ())
        rows = cur.fetchall()
        cur.close()
        return rows

    def fetch_one(self, query, params=None):
        cur = self._cursor(dictionary=True)
        cur.execute(query, params or ())
        row = cur.fetchone()
        cur.close()
        return row

    # ------------------------------------------------------------
    # Patients
    # ------------------------------------------------------------
    def add_patient(self, first_name, last_name, dob, gender, phone,
                     email, address, blood_group):
        query = """
            INSERT INTO patients
                (first_name, last_name, date_of_birth, gender, phone,
                 email, address, blood_group)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        return self.execute(
            query, (first_name, last_name, dob, gender, phone,
                    email, address, blood_group), commit=True)

    def get_patients(self, search=None):
        if search:
            query = """
                SELECT * FROM patients
                WHERE first_name LIKE %s OR last_name LIKE %s OR phone LIKE %s
                ORDER BY patient_id DESC
            """
            like = f"%{search}%"
            return self.fetch_all(query, (like, like, like))
        return self.fetch_all("SELECT * FROM patients ORDER BY patient_id DESC")

    def update_patient(self, patient_id, **fields):
        if not fields:
            return
        set_clause = ", ".join(f"{k} = %s" for k in fields)
        query = f"UPDATE patients SET {set_clause} WHERE patient_id = %s"
        self.execute(query, (*fields.values(), patient_id), commit=True)

    def delete_patient(self, patient_id):
        self.execute("DELETE FROM patients WHERE patient_id = %s",
                      (patient_id,), commit=True)

    # ------------------------------------------------------------
    # Doctors
    # ------------------------------------------------------------
    def get_doctors(self):
        query = """
SELECT d.*, dept.name AS department_name
            FROM doctors d
            LEFT JOIN departments dept ON d.department_id = dept.department_id
            ORDER BY d.doctor_id
        """
        return self.fetch_all(query)

    def add_doctor(self, first_name, last_name, specialization, phone,
                    email, department_id):
        query = """
            INSERT INTO doctors
                (first_name, last_name, specialization, phone, email, department_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return self.execute(
            query, (first_name, last_name, specialization, phone,
                    email, department_id), commit=True)

    # ------------------------------------------------------------
    # Appointments
    # ------------------------------------------------------------
    def add_appointment(self, patient_id, doctor_id, appointment_date, reason):
        query = """
            INSERT INTO appointments
                (patient_id, doctor_id, appointment_date, reason)
            VALUES (%s, %s, %s, %s)
        """
        return self.execute(
            query, (patient_id, doctor_id, appointment_date, reason), commit=True)

    def get_appointments(self):
        query = """
            SELECT a.appointment_id, p.first_name AS patient_first,
                   p.last_name AS patient_last, d.first_name AS doctor_first,
                   d.last_name AS doctor_last, a.appointment_date,
                   a.reason, a.status
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            ORDER BY a.appointment_date DESC
        """
        return self.fetch_all(query)

    def update_appointment_status(self, appointment_id, status):
        self.execute(
            "UPDATE appointments SET status = %s WHERE appointment_id = %s",
            (status, appointment_id), commit=True)

    # ------------------------------------------------------------
    # Billing
    # ------------------------------------------------------------
    def add_bill(self, patient_id, appointment_id, admission_id, amount):
        query = """
            INSERT INTO billing (patient_id, appointment_id, admission_id, amount)
            VALUES (%s, %s, %s, %s)
        """
        return self.execute(
            query, (patient_id, appointment_id, admission_id, amount), commit=True)

    def get_bills(self):
        query = """
            SELECT b.bill_id, p.first_name, p.last_name, b.amount,
                   b.bill_date, b.payment_status
            FROM billing b
            JOIN patients p ON b.patient_id = p.patient_id
            ORDER BY b.bill_date DESC
        """
        return self.fetch_all(query)

    def mark_bill_paid(self, bill_id):
        self.execute(
            "UPDATE billing SET payment_status = 'Paid' WHERE bill_id = %s",
            (bill_id,), commit=True)

    # ------------------------------------------------------------
    # Users / auth
    # ------------------------------------------------------------
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username, password, role="Receptionist"):
        query = "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)"
        return self.execute(
            query, (username, self.hash_password(password), role), commit=True)

    def verify_login(self, username, password):
        query = "SELECT * FROM users WHERE username = %s"
        user = self.fetch_one(query, (username,))
        if user and user["password_hash"] == self.hash_password(password):
            return user
        return None

    def close(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
