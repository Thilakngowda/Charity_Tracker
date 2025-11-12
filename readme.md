# 🤝 Helping Hands - Charity Management System

## 🌍 Overview

**Helping Hands** is a simple yet powerful **charity management system** that helps organizations or individuals easily keep track of donors and their contributions.  
The goal of this project is to **make managing donations effortless and transparent**, all through a friendly and easy-to-use interface.

It’s a **desktop application** built using **Python (CustomTkinter)** for the frontend and **SQLite** for the backend — a perfect combination of simplicity and reliability.

---

## 💡 Why This Project?

Many small charities or NGOs rely on messy spreadsheets or paper records to track donors and donations.  
Helping Hands solves that problem by offering a clean, database-driven app that:
- Stores all donor details safely in one place  
- Records donations with automatic linking to donor IDs  
- Shows a total donation summary in real-time  
- Lets you export all data to Excel for easy reporting  

No internet needed, no complicated setup — just run and start helping. 🙌

---

## ✨ Key Features

### 🖥️ Frontend (User Interface)
- Modern, minimalist design using **CustomTkinter**
- Easy navigation between pages:
  1. **Welcome Page** – Shows the Helping Hands logo and app intro  
  2. **Donor Page** – Add new donors and record their donations  
  3. **Records Page** – View, refresh, or export donor and donation data
- Responsive buttons, neat layouts, and soft dark mode theme
- Instant updates and live total funds display
- Option to **delete all data** or **export records to Excel** for reports

---

### 🧠 Backend (Database & Logic)
- Uses **SQLite**, a lightweight built-in database
- Automatically assigns **unique Donor IDs**
- Links each donation entry to its respective donor (using foreign keys)
- Stores donor names, emails, and phone numbers
- Keeps donation amount and date of contribution
- All data is **stored locally** and **remains available** even after the app is closed

---

## 🧩 System Design

| Layer | Technology | Role |
|--------|-------------|------|
| **Frontend** | CustomTkinter | Manages the user interface and data input |
| **Logic** | Python Functions | Controls app flow and database operations |
| **Backend** | SQLite3 | Stores donor and donation data securely |

---

## ⚙️ How It Works (in simple terms)

1. You open the app and see the Helping Hands welcome screen 🌟  
2. You click “Go to Donor Page” and fill out donor details (name, email, phone).  
3. Each new donor automatically gets a **unique ID**.  
4. You record donations — the system automatically links them to the donor.  
5. The **Records Page** shows all donors and donations, plus total funds.  
6. You can **refresh, delete, or export** all data whenever you need.  

---

## 📂 Project Structure

HelpingHands/
│
├── helping_hands.py # Main program (UI + backend)
├── helping_hands.db # SQLite database (auto-created)
├── logo.png # Helping Hands logo
├── donors_data.xlsx # Exported data file (optional)
├── screenshot.png # Screenshot of app running
└── README.md # Project documentation

yaml
Copy code

---

## 🚀 How to Run the Project

### Step 1: Install Requirements
Make sure you have Python 3.11+ installed. Then open a terminal and run:
```bash
pip install customtkinter darkdetect packaging openpyxl

### Step 2: Run the App
Navigate to the folder containing helping_hands.py and run:

bash
Copy code
python helping_hands.py
Step 3: Explore the App
🧾 Add new donors

💰 Record donations

📊 View and export data

🧹 Clear the database if needed

Everything happens in a beautiful, interactive desktop window — no browser required.

🧾 Data Flow Summary
scss
Copy code
User (inputs donor/donation info)
        ↓
Python Logic (validates & processes)
        ↓
SQLite Database (stores securely)
        ↓
User Interface (displays live data)
🧰 Tools & Technologies
Tool	Purpose
Python 3.11	Core programming language
CustomTkinter	GUI design framework
SQLite3	Database engine
OpenPyXL	Excel export
DarkDetect	Automatic theme detection

💬 Example Use Case
Imagine you’re part of a local NGO collecting donations for school supplies.
Each donor’s name, email, and phone number can be saved instantly.
As you receive contributions, the system keeps track — showing you exactly how much has been raised overall.

At the end of the week, you can export everything to Excel and share the report with your team or supervisor.

That’s Helping Hands in action — simple, fast, and dependable.

🌱 Future Ideas
Add donor search and sorting filters
Generate printable PDF reports
Send automatic thank-you emails to donors
Built with ❤️ using Python and SQLite

🏁 Final Thoughts
The Helping Hands Charity Management System is a complete example of how a well-designed Python project can blend both a frontend (CustomTkinter) and a backend (SQLite) into one cohesive system.

It’s practical, functional, and built with real-world use in mind — showing how even simple tools can make a meaningful difference. 💚


“No one has ever become poor by giving.” – Anne Frank