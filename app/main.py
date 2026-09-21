from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from typing import List, Optional

from fastapi.middleware.cors import CORSMiddleware

from app import models, schemas
from app.database import engine, get_db

# Creates the database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Spend Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://expense-tracker-rho-gold-36.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/expenses", response_model=schemas.ExpenseOut)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = models.Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.get("/expenses", response_model=List[schemas.ExpenseOut])
def list_expenses(
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        db: Session = Depends(get_db)
):
    query = db.query(models.Expense)
    if category:
        query = query.filter(models.Expense.category == category)
    if start_date:
        query = query.filter(models.Expense.date >= start_date)
    if end_date:
        query = query.filter(models.Expense.date <= end_date)
    return query.all()


@app.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    total_spend = db.query(func.sum(models.Expense.amount)).scalar() or 0.0

    category_spend_query = db.query(
        models.Expense.category, func.sum(models.Expense.amount).label("total")
    ).group_by(models.Expense.category).all()
    spend_by_category = {cat: total for cat, total in category_spend_query}

    # Month-over-month calculation logic
    today = date.today()
    current_month_start = today.replace(day=1)

    if current_month_start.month == 1:
        prev_month_start = current_month_start.replace(year=today.year - 1, month=12)
    else:
        prev_month_start = current_month_start.replace(month=today.month - 1)

    current_month_spend = db.query(func.sum(models.Expense.amount)).filter(
        models.Expense.date >= current_month_start
    ).scalar() or 0.0

    prev_month_spend = db.query(func.sum(models.Expense.amount)).filter(
        models.Expense.date >= prev_month_start,
        models.Expense.date < current_month_start
    ).scalar() or 0.0

    if prev_month_spend == 0:
        mom_change = 100.0 if current_month_spend > 0 else 0.0
    else:
        mom_change = ((current_month_spend - prev_month_spend) / prev_month_spend) * 100

    return {
        "total_spend": total_spend,
        "spend_by_category": spend_by_category,
        "current_month_spend": current_month_spend,
        "previous_month_spend": prev_month_spend,
        "mom_change_percentage": round(mom_change, 2)
    }