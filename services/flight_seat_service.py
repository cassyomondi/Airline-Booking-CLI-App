# services/flight_seat_service.py
from models import FlightSeat

class FlightSeatService:
    def __init__(self, session):
        self.session = session

    def add_seat(self, flight_id, seat_number, seat_class, base_price=100.0):
        multipliers = {"ECONOMY": 1.0, "BUSINESS": 1.5, "FIRST": 2.0}
        multiplier = multipliers.get(seat_class.upper(), 1.0)
        price = base_price * multiplier

        seat = FlightSeat(
            flight_id=flight_id,
            seat_number=seat_number,
            seat_class=seat_class.upper(),
            price=price
        )
        self.session.add(seat)
        self.session.commit()
        return seat
