from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

from app.main import app
from app.database import Base, get_db

# Isolate testing to a separate test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_expenses.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def setup_module(module):
    Base.metadata.create_all(bind=engine)

def teardown_module(module):
    Base.metadata.drop_all(bind=engine)

def test_create_expense_happy_path():
    response = client.post(
        "/expenses",
        json={"amount": 120.0, "category": "Utilities", "note": "Electric", "date": str(date.today())}
    )
    assert response.status_code == 200
    assert response.json()["amount"] == 120.0

def test_create_expense_negative_amount_fails():
    response = client.post(
        "/expenses",
        json={"amount": -50.0, "category": "Food", "date": str(date.today())}
    )
    assert response.status_code == 422  # Unprocessable Entity (Validation Error)

def test_list_expenses_with_filters():
    response = client.get("/expenses?category=Utilities")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["category"] == "Utilities"

def test_get_summary():
    response = client.get("/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_spend" in data
    assert "spend_by_category" in data
    assert "mom_change_percentage" in data