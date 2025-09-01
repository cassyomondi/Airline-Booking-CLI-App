# test_booking_service.py
from datetime import datetime
from database import SessionLocal
from services.passenger_service import PassengerService
from services.flight_service import FlightService
from services.booking_service import BookingService
from services.flight_seat_service import FlightSeatService

def run_tests():
    print("=== Booking Service Tests ===")
    db = SessionLocal()

    passenger_service = PassengerService(db)
    flight_service = FlightService(db)
    booking_service = BookingService(db)
    seat_service = FlightSeatService(db)

    # 1. Add a passenger
    passenger = passenger_service.add_passenger(
        name="John Doe",
        email="johndoe@example.com",
        passport_number="P1234567"
    )
    print(f"✅ Added passenger: {passenger.name} ({passenger.id})")

    # 2. Add a flight
    flight = flight_service.add_flight(
        "ET202", "Addis Ababa", "Paris",
        datetime(2025, 10, 1, 8, 0, 0),
        datetime(2025, 10, 1, 14, 0, 0),
        500.00, 150
    )
    print(f"✅ Added flight: {flight.flight_number} ({flight.id})")

    # 3. Add a seat to that flight
    seat = seat_service.add_seat(flight.id, "1A", "ECONOMY")
    print(f"✅ Added seat: {seat.seat_code} ({seat.id})")

    # 4. Book the seat
    booking = booking_service.add_booking(passenger.id, flight.id, "1A")
    print(f"✅ Booking created: {booking.id}, Seat: {seat.seat_code}, Status: {booking.status}")

    db.close()

if __name__ == "__main__":
    run_tests()
