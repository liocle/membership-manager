# Membership & Payment Tracker

## 📌 Overview
This project is a **self-hosted membership management and billing system** designed to:
- Store **member contact information** and **billing details**.
- Generate and send **invoices as PDFs**.
- Track **payments via reference number** from bank statements.
- Provide a **web-based UI for managing members and invoices**.

## 🏗️ Tech Stack
- **Database:** PostgreSQL (Dockerized)
- **Backend:** Python (Flask/FastAPI)
- **UI/Admin Panel:** NocoDB (optional) or custom React frontend
- **Automation:** Python scripts for email parsing & bank CSV processing
- **Containerization:** Docker & Docker Compose

## 🛠️ Setup Instructions
### 1️⃣ Clone the Repo
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 2️⃣ Run Database in Docker
```bash
docker-compose up -d
```
This starts **PostgreSQL** and **pgAdmin** (accessible at `http://localhost:5050`).

### 3️⃣ Initialize the Database
1. Open `pgAdmin` (`http://localhost:5050`).
2. Login with:
   - **Email:** `admin@example.com`
   - **Password:** `adminpassword`
3. Connect to the `members_db` database and run `init.sql` to create tables.

### 4️⃣ Future Steps
- Implement **email parsing** for new member entries.
- Develop **CSV ingestion** for payment reconciliation.
- Automate **invoice generation** and email sending.

## 📌 Features Roadmap
✅ PostgreSQL database with `members`, `invoices`, `payments` tables.  
🔄 Email parsing for member intake (Gmail plaintext processing).  
📥 CSV processing for payment matching (Viitenumero validation).  
📧 Automated PDF invoice generation & email delivery.  
📊 Web UI for easier data management.  

---

## 🤝 Contributions
Feel free to open issues, suggest features, or contribute via pull requests!

### **License**
MIT License - Free to use and modify. 🚀

