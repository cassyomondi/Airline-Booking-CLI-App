from sqlalchemy import Column, Integer, String
from database import Base

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True)
    flight_number = Column(String, unique=True, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    total_seats = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)
