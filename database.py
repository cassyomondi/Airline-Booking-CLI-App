from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///airline.db")  # using SQLite for now

import models  # this ensures all models are imported so metadata knows about them

# Create all tables if they don't exist
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine)
