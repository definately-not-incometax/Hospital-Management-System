"""
test_db_connector.py — Automated tests for the Hospital Management System
============================================================================
Runs real CRUD operations against the hospital_db MySQL/MariaDB database
to verify the db_connector.py module works end-to-end.

Run with:  python -m pytest tests/test_db_connector.py -v
       or:  python tests/test_db_connector.py
"""

import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "database"))
from db_connector import Database  # noqa: E402


class TestDatabaseConnection(unittest.TestCase):
    """Verify the app can connect to MariaDB/MySQL."""

    def test_connection_established(self):
        db = Database()
        self.assertTrue(db.conn.is_connected())
        db.close()


class TestPatientCRUD(unittest.TestCase):
    """Verify add / search / update / delete for patients."""

    def setUp(self):
        self.db = Database()

    def tearDown(self):
        self.db.close()

    def test_add_and_fetch_patient(self):
        new_id = self.db.add_patient(
            "Test", "Patient", "2000-01-01", "Male",
            "9999999999", "test.patient@mail.com", "Test Address", "O+")
        self.assertIsNotNone(new_id)

        results = self.db.get_patients(search="Test")
        self.assertTrue(any(p["patient_id"] == new_id for p in results))

        # cleanup
        self.db.delete_patient(new_id)

    def test_update_patient(self):
        new_id = self.db.add_patient(
            "Update", "Me", "1999-05-05", "Female",
            "8888888888", "update.me@mail.com", "Somewhere", "A+")
        self.db.update_patient(new_id, phone="7777777777")
        updated = self.db.fetch_one(
            "SELECT * FROM patients WHERE patient_id = %s", (new_id,))
        self.assertEqual(updated["phone"], "7777777777")
        self.db.delete_patient(new_id)

    def test_delete_patient(self):
        new_id = self.db.add_patient(
            "Delete", "Me", "1998-02-02", "Male",
            "6666666666", "delete.me@mail.com", "Nowhere", "B-")
        self.db.delete_patient(new_id)
        result = self.db.fetch_one(
            "SELECT * FROM patients WHERE patient_id = %s", (new_id,))
        self.assertIsNone(result)

    def test_existing_seed_patients_present(self):
        patients = self.db.get_patients()
        self.assertGreaterEqual(len(patients), 4)


class TestDoctors(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def tearDown(self):
        self.db.close()

    def test_get_doctors_returns_department_name(self):
        doctors = self.db.get_doctors()
        self.assertGreater(len(doctors), 0)
        self.assertIn("department_name", doctors[0])


class TestAppointments(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def tearDown(self):
        self.db.close()

    def test_add_and_fetch_appointment(self):
        patient_id = self.db.get_patients()[0]["patient_id"]
        doctor_id = self.db.get_doctors()[0]["doctor_id"]
        appt_id = self.db.add_appointment(
            patient_id, doctor_id, "2026-12-01 10:00:00", "Test reason")
        appts = self.db.get_appointments()
        self.assertTrue(any(a["appointment_id"] == appt_id for a in appts))

    def test_mark_appointment_completed(self):
        patient_id = self.db.get_patients()[0]["patient_id"]
        doctor_id = self.db.get_doctors()[0]["doctor_id"]
        appt_id = self.db.add_appointment(
            patient_id, doctor_id, "2026-12-02 11:00:00", "Status test")
        self.db.update_appointment_status(appt_id, "Completed")
        row = self.db.fetch_one(
            "SELECT status FROM appointments WHERE appointment_id = %s",
            (appt_id,))
        self.assertEqual(row["status"], "Completed")


class TestBilling(unittest.TestCase):
    def setUp(self):
self.db = Database()

    def tearDown(self):
        self.db.close()

    def test_add_bill_and_mark_paid(self):
        patient_id = self.db.get_patients()[0]["patient_id"]
        bill_id = self.db.add_bill(patient_id, None, None, 1500.00)
        self.db.mark_bill_paid(bill_id)
        row = self.db.fetch_one(
            "SELECT payment_status FROM billing WHERE bill_id = %s", (bill_id,))
        self.assertEqual(row["payment_status"], "Paid")


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def tearDown(self):
        self.db.close()

    def test_create_user_and_login(self):
        self.db.execute("DELETE FROM users WHERE username = %s",
                         ("testuser",), commit=True)
        self.db.create_user("testuser", "SecurePass123", role="Admin")
        user = self.db.verify_login("testuser", "SecurePass123")
        self.assertIsNotNone(user)
        self.assertEqual(user["role"], "Admin")

    def test_login_fails_with_wrong_password(self):
        self.db.execute("DELETE FROM users WHERE username = %s",
                         ("testuser2",), commit=True)
        self.db.create_user("testuser2", "CorrectPass", role="Receptionist")
        user = self.db.verify_login("testuser2", "WrongPass")
        self.assertIsNone(user)


if __name__ == "__main__":
    unittest.main(verbosity=2)
