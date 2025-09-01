# models/flight.py
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from database import Base

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    base_price = Column(DECIMAL, nullable=False)
    capacity = Column(Integer, nullable=False)

    # Relationships
    seats = relationship("FlightSeat", back_populates="flight", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="flight", cascade="all, delete-orphan")
