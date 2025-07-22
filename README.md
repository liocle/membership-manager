
# Membership Manager

A containerized FastAPI application for managing members and yearly memberships, built with modern Python tooling and an automated GitHub Actions–backed CI pipeline.

---

## 🔍 Project Overview

- **Purpose**: CRUD-style API to create, query, update, and delete members and their yearly memberships.
- **Goals**:
  1. Practice backend development with FastAPI, SQLAlchemy, and Pydantic
  2. Enforce consistent development and testing environments via Docker Compose
  3. Automate linting, testing, and coverage reporting in CI

---

## 🛠 Tech Stack

- Python 3.11
- FastAPI (HTTP API)
- SQLAlchemy + Alembic (ORM & migrations)
- Pydantic (settings & schemas)
- PostgreSQL (database)
- Docker & Docker Compose
- Make
- GitHub Actions (CI)

---

## Getting Started

1. **Clone & enter**
   ```sh
   git clone https://github.com/liocle/membership-manager.git
   cd membership-manager
    ```
2. **Set up Python**

    ```sh
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Configure environment**
- Copy `.env.example` to `.env` and adjust settings as needed.
- Ensure .env.test contains test DB.

4. **Start services**
   ```sh
   make
   ```
   - API docs: http://localhost:8000/docs

5. **Run tests**
   ```sh
    make pytest_local
    ```

## Getting Started

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


