# models/passenger.py
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from database import Base
from datetime import date

class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    passport_number = Column(String, unique=True, nullable=False)
    join_date = Column(Date, nullable=False, default=date.today)  # ✅ default value

    # Relationships
    bookings = relationship("Booking", back_populates="passenger", cascade="all, delete-orphan")
