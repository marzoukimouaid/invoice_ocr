from datetime import date
from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


Base = declarative_base()


class DBinvoice(Base):
    __tablename__ = "invoices"
    invoice_number = Column(String, primary_key=True, index=True)
    invoice_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)



class Invoice(BaseModel):
    invoice_number: str
    invoice_date: date
    amount: float

    class Config:
        from_attributes = True


DATABASE_URL = "sqlite:///./invoice_ocr.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



