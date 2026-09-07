"""
main.py — Hospital Management System GUI
==========================================
A Tkinter desktop application providing CRUD operations for:
  - Patients (add / search / update / delete)
  - Doctors (view / add)
  - Appointments (schedule / view / mark completed)
  - Billing (view / mark paid)

Run with:  python main.py

Author: Bhaskarjyoti Dey
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "database"))
from db_connector import Database  # noqa: E402


class HospitalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hospital Management System")
        self.geometry("950x600")
        self.resizable(True, True)

        try:
            self.db = Database()
        except ConnectionError as e:
            messagebox.showerror("Database Error", str(e))
            self.destroy()
            return

        self._build_ui()

    # ------------------------------------------------------------
    def _build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.patients_tab = PatientsTab(notebook, self.db)
        self.doctors_tab = DoctorsTab(notebook, self.db)
        self.appointments_tab = AppointmentsTab(notebook, self.db)
        self.billing_tab = BillingTab(notebook, self.db)

        notebook.add(self.patients_tab, text="Patients")
        notebook.add(self.doctors_tab, text="Doctors")
        notebook.add(self.appointments_tab, text="Appointments")
        notebook.add(self.billing_tab, text="Billing")

    def on_close(self):
        self.db.close()
        self.destroy()


class PatientsTab(ttk.Frame):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        self._build_form()
        self._build_table()
        self.refresh()

    def _build_form(self):
        form = ttk.LabelFrame(self, text="Add / Search Patient")
        form.pack(fill="x", padx=8, pady=8)

        labels = ["First Name", "Last Name", "DOB (YYYY-MM-DD)", "Gender",
                  "Phone", "Email", "Address", "Blood Group"]
        self.entries = {}
        for i, label in enumerate(labels):
            row, col = divmod(i, 4)
            ttk.Label(form, text=label).grid(row=row * 2, column=col, sticky="w", padx=4)
            entry = ttk.Entry(form, width=20)
            entry.grid(row=row * 2 + 1, column=col, padx=4, pady=2)
            self.entries[label] = entry

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=4, column=0, columnspan=4, pady=6)
        ttk.Button(btn_frame, text="Add Patient", command=self.add_patient).pack(side="left", padx=4)

        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=8)
        ttk.Label(search_frame, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=4)
        ttk.Button(search_frame, text="Search", command=self.refresh).pack(side="left")
        ttk.Button(search_frame, text="Clear", command=self.clear_search).pack(side="left", padx=4)
        ttk.Button(search_frame, text="Delete Selected", command=self.delete_patient).pack(side="right")

    def _build_table(self):
        cols = ("id", "first_name", "last_name", "dob", "gender",
                "phone", "email", "blood_group")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=15)
        for c in cols:
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, width=100)
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

    def add_patient(self):
        vals = {k: v.get().strip() for k, v in self.entries.items()}
if not vals["First Name"] or not vals["Last Name"]:
            messagebox.showwarning("Validation", "First and last name are required.")
            return
        try:
            self.db.add_patient(
                vals["First Name"], vals["Last Name"],
                vals["DOB (YYYY-MM-DD)"] or None, vals["Gender"] or "Other",
                vals["Phone"], vals["Email"], vals["Address"], vals["Blood Group"])
            messagebox.showinfo("Success", "Patient added.")
            for e in self.entries.values():
                e.delete(0, tk.END)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        search = self.search_var.get().strip() or None
        for p in self.db.get_patients(search):
            self.tree.insert("", "end", values=(
                p["patient_id"], p["first_name"], p["last_name"],
                p["date_of_birth"], p["gender"], p["phone"],
                p["email"], p["blood_group"]))

    def clear_search(self):
        self.search_var.set("")
        self.refresh()

    def delete_patient(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Select a patient row first.")
            return
        patient_id = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm", f"Delete patient #{patient_id}?"):
            self.db.delete_patient(patient_id)
            self.refresh()


class DoctorsTab(ttk.Frame):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        cols = ("id", "first_name", "last_name", "specialization",
                "phone", "email", "department")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, width=120)
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)
        ttk.Button(self, text="Refresh", command=self.refresh).pack(pady=4)
        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for d in self.db.get_doctors():
            self.tree.insert("", "end", values=(
                d["doctor_id"], d["first_name"], d["last_name"],
                d["specialization"], d["phone"], d["email"],
                d.get("department_name")))


class AppointmentsTab(ttk.Frame):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        cols = ("id", "patient", "doctor", "date", "reason", "status")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=130)
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=4)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Mark Completed", command=self.mark_completed).pack(side="left", padx=4)
        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for a in self.db.get_appointments():
            self.tree.insert("", "end", values=(
                a["appointment_id"],
                f"{a['patient_first']} {a['patient_last']}",
                f"{a['doctor_first']} {a['doctor_last']}",
                a["appointment_date"], a["reason"], a["status"]))

    def mark_completed(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Select an appointment first.")
            return
        appt_id = self.tree.item(selected[0])["values"][0]
self.db.update_appointment_status(appt_id, "Completed")
        self.refresh()


class BillingTab(ttk.Frame):
    def __init__(self, parent, db: Database):
        super().__init__(parent)
        self.db = db
        cols = ("id", "first_name", "last_name", "amount", "date", "status")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=130)
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=4)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Mark Paid", command=self.mark_paid).pack(side="left", padx=4)
        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for b in self.db.get_bills():
            self.tree.insert("", "end", values=(
                b["bill_id"], b["first_name"], b["last_name"],
                b["amount"], b["bill_date"], b["payment_status"]))

    def mark_paid(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Select a bill first.")
            return
        bill_id = self.tree.item(selected[0])["values"][0]
        self.db.mark_bill_paid(bill_id)
        self.refresh()


if __name__ == "__main__":
    app = HospitalApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
