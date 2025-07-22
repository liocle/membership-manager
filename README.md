# Membership Manager

A containerized FastAPI application for managing members and yearly memberships, built with modern Python tooling and an automated GitHub Actions–backed CI pipeline.

---

## 🔍 Project Overview

- **Purpose**: CRUD‑style API to create, query, update, and delete members and their yearly memberships.
- **Goals**:
  1. Practice backend development with FastAPI, SQLAlchemy, and Pydantic
  2. Enforce consistent development and testing environments via Docker Compose
  3. Automate linting, testing, and coverage reporting in CI
  4. Generate PDF welcome letters for new or existing members

---

## 🛠 Tech Stack

- Python 3.11
- FastAPI (HTTP API)
- SQLAlchemy + Alembic (ORM & migrations)
- Pydantic (settings & schemas)
- PostgreSQL
- Docker & Docker Compose 
- Make
- GitHub Actions (CI)
- WeasyPrint & Jinja2 (PDF generation)

---

## 🚀 Getting Started

1. **Clone & enter**

   ```bash
   git clone https://github.com/liocle/membership-manager.git
   cd membership-manager
   ```

2. **Set up Python**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r app/requirements.txt
   ```

3. **Configure environment**

   - Copy `.env.example` to `.env` and fill in values
   - Ensure `.env.test` contains test DB settings

4. **Start services**

   ```bash
   make
   ```

   - API docs: http://localhost:8000/docs
   - PDF letters are saved to output/letters/ by default

---

## ✅ CI & Branch Protection

- **Workflow file**: `.github/workflows/ci.yml`
- **Triggers**: `pull_request` and manual via `workflow_dispatch`
- **Jobs**:
  1. **Lint & Format Check** (`ruff`, `black --check`)
  2. **Python Tests & Coverage** (`pytest --cov=app`, uploads `coverage.xml`)

**Branch protection** on `main` requires:
- Passing **Python Tests & Coverage** status check
- Lint check executed but do not fail PRs
- PDF Generation Tests

---

## 🧪 Testing & Coverage

Run tests locally with coverage:

```bash
make pytest_local
```

This will:
- Spin up Postgres via Docker Compose
- Recreate the test database
- Execute `pytest` with:
  - `--cov=app`
  - `--cov-report=term-missing`
  - `--cov-report=xml`
  - `--cov-report=html`

Artifacts:
- `coverage.xml` (CI artifact)
- `htmlcov/index.html` (open in browser)

---

## 📁 Project Structure

```
membership-manager/
├─ .github/workflows/ci.yml
├─ docker-compose.yml
├─ Makefile
├─ .env, .env.test
├─ app/
│  ├─ api/          # route modules
│  ├─ models.py     # SQLAlchemy models
│  ├─ schemas.py    # Pydantic schemas
│  ├─ config.py     # settings loader
│  ├─ create_tables.py
│  ├─ database.py
│  └─ pdf/          # PDF generation scripts & templates
│     ├─ generate_welcome_letter.py
│     └─ templates/
│        └─ welcome_letter.html.jinja2
├─ output/
│  └─ letters/      # Generated PDF files (gitignored)
├─ tests/           # pytest suite
│  └─ test_generate_welcome_letter_route.py
├─ coverage.xml     # coverage artifact
├─ htmlcov/         # HTML coverage report
└─ requirements.txt
```

---

## ⚙️ Makefile

- `make`                – start Postgres, API & pgAdmin
- `make pytest_local`   – run tests with coverage reports
- `make create_db`      – run DB init script
- `make seed_db`        – seed sample data
- `make help`           – display full command list
---

## 📄 License

MIT © 2025 Lionel Clerc
