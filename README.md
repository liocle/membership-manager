
# **Membership Manager**

## **📌 Project Overview**
Membership Manager is a database-driven web application designed to streamline the management of a user base, including member records, subscriptions, and payment tracking. The goal is to replace an outdated system with a modern, maintainable solution that improves accuracy and efficiency.

This project is a personal initiative to deepen my backend development and DevOps skills by building a full-stack application from scratch with real-world features and infrastructure.

## **🛠️ Tech Stack**

### **Backend**
- **Python** (Core backend logic)
- **FastAPI** (High-performance web framework for API development)
- **SQLAlchemy** (ORM for database modeling)
- **Alembic** (Database migrations and schema versioning)
- **PostgreSQL** (Relational database)

### **Infrastructure & Deployment**
- **Docker & Docker Compose** (Containerized local development and deployment)
- **GitHub Actions** (CI pipeline for testing and integration)

### **Testing & Development Tools**
- **Pytest** (Unit and integration tests)
- **pgAdmin** (Database visualization and admin)
- **direnv** – Environment variable loader
- **make** – One-command workflows

## **✅ Current Features**
- **RESTful API**: Core endpoints for creating, updating, deleting, and searching members and their yearly memberships
- **Automatic Membership Creation**: New members receive an unpaid membership by default (configurable)
- **Config-Driven Logic**: `.env` file powers key values (e.g. standard fee) using a central `config.py` module
- **Auto-generated Fields**: Computed `full_name` field (via SQL) for better searching and display
- **Dockerized Environment**: One-command setup with Docker Compose
- **Database Seeding**: Sample data and full DB reset supported via `make` commands
- **CI Pipeline Setup**: GitHub Actions configured and validated with placeholder tests; ready for integration with real test coverage.
- **Database Seeding**: Sample data scripts for dev and test environments
- **First Release Milestone**: Tagged as `api-basics` 

## **🚧 MVP Goals (In Progress)**
- **CSV Import for Payment Updates**: Script to mark memberships as paid based on bank statements
- **PDF Letter Generation**: Welcome letters for newly registered members (WeasyPrint)
- **Basic Admin UI**: React-based interface for manual corrections

## ▶️ Getting Started

```bash
# Clone the repository
git clone https://github.com/liocle/membership-manager.git
cd membership-manager

# Run development environment
make dev

# API documentation available at:
http://localhost:8000/docs
```


## 🛠 Developer Setup

This project uses:

- `pyenv` for Python version management (`.python-version`)
- `venv` for isolated dependencies (`.venv/`)
- `direnv` for automatic environment loading (`.envrc`, `.env`)
- `pip` + `requirements.txt` for dependency tracking

### One-time setup:
```bash
pyenv install 3.11.9
pyenv local 3.11.9
python -m venv .venv
direnv allow
pip install -r requirements.txt
```

## 👤 Author
Created and maintained by **Lionel Clerc**. This project serves as a foundation for learning and building backend services using modern Python tools and DevOps practices.


