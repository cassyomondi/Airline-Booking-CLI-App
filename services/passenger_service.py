# services/passenger_service.py
from models.passenger import Passenger
from datetime import datetime
from sqlalchemy.orm import Session

class PassengerService:
    def __init__(self, db: Session):
        self.db = db

    def add_passenger(self, name: str, email: str, passport_number: str):
        passenger = Passenger(
            name=name,
            email=email,
            passport_number=passport_number,
            join_date=datetime.utcnow()  # ✅ auto-set join date
        )
        self.db.add(passenger)
        self.db.commit()
        self.db.refresh(passenger)
        return passenger

    def get_passenger_by_id(self, passenger_id: int):
        return self.db.query(Passenger).filter(Passenger.id == passenger_id).first()

    def get_all_passengers(self):
        return self.db.query(Passenger).all()

    def delete_passenger(self, passenger_id: int):
        passenger = self.get_passenger_by_id(passenger_id)
        if passenger:
            self.db.delete(passenger)
            self.db.commit()
            return True
        return False
