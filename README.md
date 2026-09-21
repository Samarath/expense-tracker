# Spend Tracker API & Minimal UI

A full-stack expense tracking application built for the Infinity Consultants technical evaluation.

## Tech Stack
* **Backend:** Python, FastAPI, SQLite, SQLAlchemy, Pydantic, Pytest
* **Frontend:** React (Vite)

## Key Design Decisions
1. **FastAPI & Pydantic:** Chosen for rapid development, built-in Swagger UI documentation, and out-of-the-box request validation.
2. **SQLite:** Used for the database as requested for simplicity, but abstracted via SQLAlchemy to make migrating to a production DB seamless.
3. **Monorepo Structure:** Both backend and frontend are kept in a single repository for easier review and deployment.
4. **Insight Bonus:** The `/summary` endpoint automatically calculates Month-over-Month (MoM) spend and flags a warning if category spend increases by more than 20%.

## How to Run Locally

### 1. Backend
```bash
# Activate virtual environment
python -m venv venv
source venv/bin/activate # On Windows: .\venv\Scripts\Activate.ps1

# Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic pytest httpx

# Run the server
uvicorn app.main:app --reload