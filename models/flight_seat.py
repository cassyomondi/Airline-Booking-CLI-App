# models/flight_seat.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class FlightSeat(Base):
    __tablename__ = "flight_seats"

    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    seat_code = Column(String, nullable=False)
    cabin_class = Column(String, nullable=False)  # ECONOMY, BUSINESS, etc.
    status = Column(String, default="AVAILABLE")  # AVAILABLE, BOOKED, HELD

    # Relationships
    flight = relationship("Flight", back_populates="seats")
    booking = relationship("Booking", back_populates="flight_seat", uselist=False)
