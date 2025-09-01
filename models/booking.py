# models/booking.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Float
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    passenger_id = Column(Integer, ForeignKey("passengers.id"), nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    flight_seat_id = Column(Integer, ForeignKey("flight_seats.id"), unique=True, nullable=False)
    booking_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="PENDING")  # PENDING, CONFIRMED, CANCELLED, HELD
    hold_expires_at = Column(DateTime, nullable=True)
    price = Column(Float, nullable=True)

    # Relationships
    passenger = relationship("Passenger", back_populates="bookings")
    flight = relationship("Flight", back_populates="bookings")
    flight_seat = relationship("FlightSeat", back_populates="booking")
