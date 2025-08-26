from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///airline_booking.db")  # using SQLite for now
SessionLocal = sessionmaker(bind=engine)
