from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String, index=True, nullable=False)
    note = Column(String)
    date = Column(Date, index=True, nullable=False)