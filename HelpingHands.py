import customtkinter as ctk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
from PIL import Image
import pandas as pd

# ---------- DATABASE SETUP ----------
conn = sqlite3.connect("charity.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS donors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS donations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_id INTEGER,
    amount REAL,
    date TEXT,
    FOREIGN KEY(donor_id) REFERENCES donors(id)
)
""")
conn.commit()

# ---------- FUNCTIONS ----------

def get_next_donor_id():
    cur.execute("SELECT seq FROM sqlite_sequence WHERE name='donors'")
    result = cur.fetchone()
    next_id = (result[0] + 1) if result else 1
    id_entry.delete(0, "end")
    id_entry.insert(0, str(next_id))

def add_donor():
    id_text = id_entry.get().strip()
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "Donor name is required!")
        return

    try:
        cur.execute("INSERT INTO donors (id, name, email, phone) VALUES (?, ?, ?, ?)", 
                    (id_text, name, email, phone))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", f"ID {id_text} already exists. Please refresh or clear and try again.")
        return

    messagebox.showinfo("Success", f"Donor '{name}' added successfully with ID: {id_text}")
    name_entry.delete(0, "end")
    email_entry.delete(0, "end")
    phone_entry.delete(0, "end")
    show_donors()
    get_next_donor_id()

def record_donation():
    donor_id = donor_id_entry.get().strip()
    amount = amount_entry.get().strip()

    if not donor_id or not amount:
        messagebox.showerror("Error", "Donor ID and Amount are required!")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Invalid amount!")
        return

    cur.execute("SELECT name FROM donors WHERE id=?", (donor_id,))
    donor = cur.fetchone()
    if not donor:
        messagebox.showerror("Error", "Invalid Donor ID! Please register the donor first.")
        return

    cur.execute("INSERT INTO donations (donor_id, amount, date) VALUES (?, ?, ?)",
                (donor_id, amount, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    messagebox.showinfo("Success", f"Donation recorded for {donor[0]}!")

    donor_id_entry.delete(0, "end")
    amount_entry.delete(0, "end")

    show_donations()
    update_total()

def show_donors():
    for item in donor_table.get_children():
        donor_table.delete(item)
    cur.execute("SELECT * FROM donors")
    for row in cur.fetchall():
        donor_table.insert("", "end", values=row)
    update_total()

def show_donations():
    for item in donation_table.get_children():
        donation_table.delete(item)
    # 👇 Fixed query to show donor_id as first column instead of donation.id
    cur.execute("""
    SELECT donors.id AS Donor_ID, donors.name AS Donor_Name, donations.amount, donations.date
    FROM donations
    JOIN donors ON donations.donor_id = donors.id
    ORDER BY donations.date DESC
    """)
    for row in cur.fetchall():
        donation_table.insert("", "end", values=row)

def update_total():
    cur.execute("SELECT SUM(amount) FROM donations")
    total = cur.fetchone()[0]
    total_label.configure(text=f"💰 Total Funds: ₹{total if total else 0}")

def delete_all_data():
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete all data?")
    if confirm:
        cur.execute("DELETE FROM donations")
        cur.execute("DELETE FROM donors")
        cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('donors', 'donations')")
        conn.commit()
        show_donors()
        show_donations()
        update_total()
        get_next_donor_id()
        messagebox.showinfo("Success", "All records deleted successfully!")

def export_to_excel():
    donor_df = pd.read_sql_query("SELECT * FROM donors", conn)
    donation_df = pd.read_sql_query("""
        SELECT donors.id AS Donor_ID, donors.name AS Donor_Name, donations.amount, donations.date
        FROM donations
        JOIN donors ON donations.donor_id = donors.id
    """, conn)
    
    with pd.ExcelWriter("Charity_Records.xlsx") as writer:
        donor_df.to_excel(writer, sheet_name="Donors", index=False)
        donation_df.to_excel(writer, sheet_name="Donations", index=False)
    
    messagebox.showinfo("Exported", "Data successfully exported to 'Charity_Records.xlsx'!")

# ---------- MAIN APP ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Helping Hands - Charity Management System")

# 👇 Make window larger (1366x768) for full screen experience
app.geometry("1366x768")

# ---------- PAGE CONTROLLER ----------
def show_frame(frame):
    frame.tkraise()

# ---------- FRAME 1: WELCOME ----------
welcome_frame = ctk.CTkFrame(app)
welcome_frame.grid(row=0, column=0, sticky="nsew")

try:
    logo_img = ctk.CTkImage(dark_image=Image.open("logo.png"), size=(200, 200))
    logo_label = ctk.CTkLabel(welcome_frame, image=logo_img, text="")
    logo_label.pack(pady=30)
except Exception:
    ctk.CTkLabel(welcome_frame, text="[Logo Missing]", font=("Arial", 18)).pack(pady=30)

ctk.CTkLabel(welcome_frame, text="🤝 Helping Hands 🤝", font=("Arial Rounded MT Bold", 36)).pack(pady=10)
ctk.CTkLabel(welcome_frame, text="Making the world better, one donation at a time.", font=("Arial", 18)).pack(pady=5)
ctk.CTkButton(welcome_frame, text="➡ Go to Donor Page", width=240, height=40, command=lambda: show_frame(donor_frame)).pack(pady=50)

# ---------- FRAME 2: ADD DONOR / DONATION ----------
donor_frame = ctk.CTkFrame(app)
donor_frame.grid(row=0, column=0, sticky="nsew")

ctk.CTkLabel(donor_frame, text="✍️ Donor Registration", font=("Arial Rounded MT Bold", 28)).pack(pady=15)

form = ctk.CTkFrame(donor_frame)
form.pack(pady=10)

ctk.CTkLabel(form, text="Donor ID:").grid(row=0, column=0, padx=10, pady=5)
id_entry = ctk.CTkEntry(form, width=240)
id_entry.grid(row=0, column=1, padx=10, pady=5)

ctk.CTkLabel(form, text="Name:").grid(row=1, column=0, padx=10, pady=5)
name_entry = ctk.CTkEntry(form, width=240)
name_entry.grid(row=1, column=1, padx=10, pady=5)

ctk.CTkLabel(form, text="Email:").grid(row=2, column=0, padx=10, pady=5)
email_entry = ctk.CTkEntry(form, width=240)
email_entry.grid(row=2, column=1, padx=10, pady=5)

ctk.CTkLabel(form, text="Phone:").grid(row=3, column=0, padx=10, pady=5)
phone_entry = ctk.CTkEntry(form, width=240)
phone_entry.grid(row=3, column=1, padx=10, pady=5)

ctk.CTkButton(donor_frame, text="➕ Add Donor", command=add_donor, width=200, height=35).pack(pady=10)

# Donation entry
ctk.CTkLabel(donor_frame, text="💰 Record Donation", font=("Arial Rounded MT Bold", 26)).pack(pady=10)

donate_form = ctk.CTkFrame(donor_frame)
donate_form.pack(pady=10)

ctk.CTkLabel(donate_form, text="Donor ID:").grid(row=0, column=0, padx=10, pady=5)
donor_id_entry = ctk.CTkEntry(donate_form, width=120)
donor_id_entry.grid(row=0, column=1, padx=10, pady=5)

ctk.CTkLabel(donate_form, text="Amount (₹):").grid(row=0, column=2, padx=10, pady=5)
amount_entry = ctk.CTkEntry(donate_form, width=120)
amount_entry.grid(row=0, column=3, padx=10, pady=5)

ctk.CTkButton(donate_form, text="✅ Record Donation", command=record_donation, width=180, height=35).grid(row=0, column=4, padx=10)

ctk.CTkButton(donor_frame, text="📋 View Donor List", command=lambda: [show_frame(list_frame), show_donors(), show_donations()]).pack(pady=20)
ctk.CTkButton(donor_frame, text="🏠 Back to Home", command=lambda: show_frame(welcome_frame)).pack()

# ---------- FRAME 3: DONOR LIST ----------
list_frame = ctk.CTkFrame(app)
list_frame.grid(row=0, column=0, sticky="nsew")

ctk.CTkLabel(list_frame, text="📋 Donor & Donation Records", font=("Arial Rounded MT Bold", 30)).pack(pady=20)

donor_table = ttk.Treeview(list_frame, columns=("ID", "Name", "Email", "Phone"), show="headings", height=6)
for col in ("ID", "Name", "Email", "Phone"):
    donor_table.heading(col, text=col)
    donor_table.column(col, width=240)
donor_table.pack(padx=10, pady=10, fill="x")

donation_table = ttk.Treeview(list_frame, columns=("Donor_ID", "Donor_Name", "Amount", "Date"), show="headings", height=6)
for col in ("Donor_ID", "Donor_Name", "Amount", "Date"):
    donation_table.heading(col, text=col)
    donation_table.column(col, width=240)
donation_table.pack(padx=10, pady=10, fill="x")

total_label = ctk.CTkLabel(list_frame, text="💰 Total Funds: ₹0", font=("Arial Rounded MT Bold", 20))
total_label.pack(pady=10)

button_frame = ctk.CTkFrame(list_frame)
button_frame.pack(pady=10)

ctk.CTkButton(button_frame, text="🔄 Refresh Data", fg_color="green", command=lambda: [show_donors(), show_donations(), get_next_donor_id()]).grid(row=0, column=0, padx=10)
ctk.CTkButton(button_frame, text="🗑 Delete All Data", fg_color="red", command=delete_all_data).grid(row=0, column=1, padx=10)
ctk.CTkButton(button_frame, text="📤 Export to Excel", fg_color="orange", command=export_to_excel).grid(row=0, column=2, padx=10)
ctk.CTkButton(button_frame, text="⬅ Back to Donor Page", fg_color="gray", command=lambda: show_frame(donor_frame)).grid(row=0, column=3, padx=10)

# ---------- INITIALIZE ----------
show_frame(welcome_frame)
show_donors()
show_donations()
update_total()
get_next_donor_id()

app.mainloop()
conn.close()
