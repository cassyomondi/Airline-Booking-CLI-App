# test_passenger_service.py
from database import SessionLocal
from services.passenger_service import PassengerService

def run_tests():
    db = SessionLocal()
    service = PassengerService(db)

    print("=== Passenger Service Tests ===")

    # 1. Add Passenger
    try:
        passenger = service.add_passenger(
            name="John Doe",
            email="john@example.com",
            passport_number="A1234567"
        )
        print(f"✅ Added passenger: {passenger.id}, {passenger.name}")
    except Exception as e:
        print(f"❌ Add passenger failed: {e}")

    # 2. Get Passenger by ID
    passenger = service.get_passenger_by_id(1)
    if passenger:
        print(f"✅ Retrieved by ID: {passenger.id}, {passenger.name}")
    else:
        print("❌ Passenger not found by ID")

    # 3. List Passengers
    passengers = service.get_all_passengers()
    print(f"✅ Total passengers: {len(passengers)}")

    # 4. Delete Passenger
    deleted = service.delete_passenger(1)
    if deleted:
        print("✅ Deleted passenger with ID 1")
    else:
        print("❌ Failed to delete passenger with ID 1")

    db.close()


if __name__ == "__main__":
    run_tests()
