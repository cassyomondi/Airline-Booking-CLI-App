# test_flightseat_service.py
from services.flight_seat_service import FlightSeatService
from services.flight_service import FlightService
from database import SessionLocal
from datetime import datetime

def run_tests():
    print("=== FlightSeat Service Tests ===")
    session = SessionLocal()
    seat_service = FlightSeatService(session)
    flight_service = FlightService(session)

    try:
        # 1. Add a flight
        flight = flight_service.add_flight(
            flight_number="ET200",
            origin="Addis Ababa",
            destination="Dubai",
            departure_time=datetime(2025, 9, 5, 14, 0, 0),
            arrival_time=datetime(2025, 9, 5, 18, 30, 0),
            base_price=350.00,
            capacity=180
        )
        print(f"✅ Added flight: {flight.id}, {flight.flight_number}")

        # 2. Add seats to that flight
        seat1 = seat_service.add_seat(flight.id, "1A", "ECONOMY")
        seat2 = seat_service.add_seat(flight.id, "1B", "ECONOMY")
        print(f"✅ Added seats: {seat1.seat_code}, {seat2.seat_code}")

        # 3. Retrieve seat by ID
        retrieved = seat_service.get_seat_by_id(seat1.id)
        assert retrieved is not None
        print(f"✅ Retrieved seat by ID: {retrieved.id}, {retrieved.seat_code}")

        # 4. List all seats for the flight
        all_seats = seat_service.list_seats_for_flight(flight.id)
        print(f"✅ Total seats for flight {flight.flight_number}: {len(all_seats)}")

        # 5. Delete one seat
        seat_service.delete_seat(seat2.id)
        print(f"✅ Deleted seat with ID {seat2.id}")

        # 6. Confirm deletion
        deleted = seat_service.get_seat_by_id(seat2.id)
        assert deleted is None
        print("✅ Seat not found after delete")

    except Exception as e:
        print(f"❌ FlightSeat Service test failed: {e}")

    finally:
        session.close()


if __name__ == "__main__":
    run_tests()
