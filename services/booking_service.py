# services/booking_service.py
from datetime import datetime
from decimal import Decimal
from models import Booking, Flight, FlightSeat

class BookingService:
    def __init__(self, db):
        self.db = db

    def create_booking(self, passenger_id, flight_id, seat_id):
        # Check if seat already booked
        existing = self.db.query(Booking).filter_by(flight_seat_id=seat_id, status="CONFIRMED").first()
        if existing:
            raise Exception("Seat already booked")

        # Get flight and seat
        flight = self.db.query(Flight).filter_by(id=flight_id).first()
        seat = self.db.query(FlightSeat).filter_by(id=seat_id).first()
        if not flight or not seat:
            raise Exception("Invalid flight or seat")

        # Calculate days to departure
        days_to_departure = (flight.departure_time - datetime.utcnow()).days

        # Ensure price is Decimal
        base_price = Decimal(flight.base_price)

        if days_to_departure >= 30:
            price = base_price * Decimal('0.8')  # early-bird discount
        elif days_to_departure <= 7:
            price = base_price * Decimal('1.2')  # late-booking surcharge
        else:
            price = base_price

        booking = Booking(
            passenger_id=passenger_id,
            flight_id=flight_id,
            flight_seat_id=seat_id,
            status="CONFIRMED",
            price=price,
        )
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def expire_holds(self):
        now = datetime.utcnow()
        expired = self.db.query(Booking).filter(
            Booking.status == "HELD",
            Booking.hold_expires_at < now
        ).all()

        for booking in expired:
            booking.status = "CANCELLED"

        self.db.commit()
        return expired
