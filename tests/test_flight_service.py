# test_flight_service.py
from services.flight_service import FlightService
from database import SessionLocal, Base, engine
from datetime import datetime

def run_tests():
    print("=== Flight Service Tests ===")
    session = SessionLocal()
    service = FlightService(session)

    try:
        # 1. Add flight
        flight = service.add_flight(
            flight_number="KQ100",
            origin="Nairobi",
            destination="London",
            departure_time=datetime(2025, 9, 1, 10, 0, 0),
            arrival_time=datetime(2025, 9, 1, 18, 0, 0),
            base_price=400.00,
            capacity=200
        )
        print(f"✅ Added flight: {flight.id}, {flight.flight_number}")

        # 2. Retrieve by ID
        retrieved = service.get_flight(flight.id)
        assert retrieved is not None
        print(f"✅ Retrieved by ID: {retrieved.id}, {retrieved.flight_number}")

        # 3. List all flights
        all_flights = service.list_flights()
        print(f"✅ Total flights: {len(all_flights)}")

    except Exception as e:
        print(f"❌ Flight Service test failed: {e}")

    finally:
        session.close()


if __name__ == "__main__":
    run_tests()
