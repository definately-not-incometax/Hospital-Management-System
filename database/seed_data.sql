-- ============================================================
-- Sample seed data for demo/testing purposes
-- ============================================================
USE hospital_db;

INSERT INTO departments (name, location) VALUES
    ('Cardiology', 'Block A, 2nd Floor'),
    ('Orthopedics', 'Block B, 1st Floor'),
    ('General Medicine', 'Block A, 1st Floor'),
    ('Pediatrics', 'Block C, Ground Floor');

INSERT INTO doctors (first_name, last_name, specialization, phone, email, department_id) VALUES
    ('Anirban', 'Chatterjee', 'Cardiologist', '9830011122', 'anirban.c@hospital.com', 1),
    ('Priya', 'Sharma', 'Orthopedic Surgeon', '9830022233', 'priya.s@hospital.com', 2),
    ('Rajesh', 'Verma', 'General Physician', '9830033344', 'rajesh.v@hospital.com', 3),
    ('Sneha', 'Roy', 'Pediatrician', '9830044455', 'sneha.r@hospital.com', 4);

INSERT INTO patients (first_name, last_name, date_of_birth, gender, phone, email, address, blood_group) VALUES
    ('Arjun', 'Dutta', '1990-05-14', 'Male', '9123456780', 'arjun.d@mail.com', 'Salt Lake, Kolkata', 'B+'),
    ('Mitali', 'Ghosh', '1985-11-02', 'Female', '9123456781', 'mitali.g@mail.com', 'Behala, Kolkata', 'O+'),
    ('Rohan', 'Basak', '2001-07-23', 'Male', '9123456782', 'rohan.b@mail.com', 'Dumdum, Kolkata', 'A-'),
    ('Ishita', 'Sen', '1995-03-30', 'Female', '9123456783', 'ishita.s@mail.com', 'Barrackpore, Kolkata', 'AB+');

INSERT INTO appointments (patient_id, doctor_id, appointment_date, reason, status) VALUES
    (1, 1, '2026-09-10 10:00:00', 'Chest pain follow-up', 'Scheduled'),
    (2, 3, '2026-09-11 11:30:00', 'General checkup', 'Scheduled'),
    (3, 2, '2026-09-05 09:00:00', 'Knee pain', 'Completed'),
    (4, 4, '2026-09-06 14:00:00', 'Routine vaccination', 'Completed');

INSERT INTO admissions (patient_id, doctor_id, room_number, admit_date, discharge_date, diagnosis) VALUES
    (3, 2, 'B-204', '2026-09-01', '2026-09-05', 'Ligament tear - post-surgery recovery');

INSERT INTO prescriptions (appointment_id, medicine_name, dosage, duration_days, notes) VALUES
    (3, 'Ibuprofen', '400mg twice daily', 7, 'Take after meals'),
    (4, 'Paracetamol Syrup', '5ml once daily', 3, 'For mild fever post-vaccination');

INSERT INTO billing (patient_id, appointment_id, admission_id, amount, payment_status) VALUES
    (1, 1, NULL, 800.00, 'Pending'),
    (2, 2, NULL, 500.00, 'Pending'),
    (3, 3, 1, 45000.00, 'Paid'),
    (4, 4, NULL, 300.00, 'Paid');

INSERT INTO staff (first_name, last_name, role, phone, department_id) VALUES
    ('Kavita', 'Nair', 'Nurse', '9876500011', 1),
    ('Debashish', 'Mondal', 'Receptionist', '9876500022', NULL);

INSERT INTO medicines (name, manufacturer, unit_price, stock_quantity) VALUES
    ('Ibuprofen', 'Cipla', 2.50, 500),
    ('Paracetamol Syrup', 'Sun Pharma', 45.00, 120),
    ('Amoxicillin', 'Zydus', 5.75, 300);
