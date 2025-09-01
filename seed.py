# seed.py
from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from database import Base
from models.flight import Flight
from models.passenger import Passenger
from models.flight_seat import FlightSeat
from models.booking import Booking

# --- Setup DB ---
engine = create_engine("sqlite:///airline.db", echo=True, future=True)

# Drop and recreate tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def seed_data():
    session = Session(bind=engine)

    # --- Add Flights ---
    flight1 = Flight(
        flight_number="KQ101",
        origin="Nairobi",
        destination="Mombasa",
        departure_time=datetime.utcnow() + timedelta(days=1),
        arrival_time=datetime.utcnow() + timedelta(days=1, hours=1),
        base_price=5000.0,
        capacity=3
    )

    flight2 = Flight(
        flight_number="ET202",
        origin="Addis Ababa",
        destination="Nairobi",
        departure_time=datetime.utcnow() + timedelta(days=2),
        arrival_time=datetime.utcnow() + timedelta(days=2, hours=2),
        base_price=8000.0,
        capacity=2
    )

    session.add_all([flight1, flight2])
    session.flush()  # Get IDs before adding seats

    # --- Add Seats ---
    seats = [
        FlightSeat(flight_id=flight1.id, seat_code="1A", cabin_class="ECONOMY"),
        FlightSeat(flight_id=flight1.id, seat_code="1B", cabin_class="ECONOMY"),
        FlightSeat(flight_id=flight1.id, seat_code="1C", cabin_class="BUSINESS"),

        FlightSeat(flight_id=flight2.id, seat_code="2A", cabin_class="ECONOMY"),
        FlightSeat(flight_id=flight2.id, seat_code="2B", cabin_class="BUSINESS"),
    ]
    session.add_all(seats)

    # --- Add Passengers ---
    passenger1 = Passenger(
        name="Alice Kimani",
        email="alice@example.com",
        passport_number="A1234567",
        join_date=date.today()
    )

    passenger2 = Passenger(
        name="John Doe",
        email="john@example.com",
        passport_number="B9876543",
        join_date=date.today()
    )

    session.add_all([passenger1, passenger2])
    session.flush()

    # --- Add Bookings ---
    booking1 = Booking(
        passenger_id=passenger1.id,
        flight_id=flight1.id,
        flight_seat_id=seats[0].id,  # 1A
        price=5000.0,
        status="CONFIRMED"
    )

    booking2 = Booking(
        passenger_id=passenger2.id,
        flight_id=flight2.id,
        flight_seat_id=seats[3].id,  # 2A
        price=8000.0,
        status="PENDING"
    )

    session.add_all([booking1, booking2])

    # Commit everything
    session.commit()
    session.close()
    print("✅ Database reseeded successfully!")

if __name__ == "__main__":
    seed_data()
