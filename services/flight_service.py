# services/flight_service.py
from models.flight import Flight
from sqlalchemy.orm import Session

class FlightService:
    def __init__(self, db: Session):
        self.db = db

    def add_flight(self, flight_number, origin, destination, departure_time, arrival_time, base_price, capacity):
        flight = Flight(
            flight_number=flight_number,
            origin=origin,
            destination=destination,
            departure_time=departure_time,
            arrival_time=arrival_time,
            base_price=base_price,
            capacity=capacity
        )
        self.db.add(flight)
        self.db.commit()
        self.db.refresh(flight)   # ✅ consistency
        return flight

    def get_flight(self, flight_id: int):
        return self.db.query(Flight).filter_by(id=flight_id).first()

    def list_flights(self):
        return self.db.query(Flight).all()
