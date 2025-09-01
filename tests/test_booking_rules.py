# tests/test_booking_rules.py
import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from models import Flight, FlightSeat, Booking, Passenger
from services.booking_service import BookingService


@pytest.fixture
def setup_data(test_db):
    # Departure 40 days from now ensures early booking
    future_departure = datetime.utcnow() + timedelta(days=40)
    flight = Flight(
        flight_number="AB123",
        origin="NYC",
        destination="LAX",
        departure_time=future_departure,
        arrival_time=future_departure + timedelta(hours=4),
        base_price=Decimal("100.00"),
        capacity=180,
    )
    test_db.add(flight)
    test_db.commit()
    test_db.refresh(flight)

    seat = FlightSeat(seat_code="1A", cabin_class="ECONOMY", flight_id=flight.id)
    test_db.add(seat)
    test_db.commit()
    test_db.refresh(seat)

    return {"flight": flight, "seat": seat}


def create_passenger(test_db, name):
    passenger = Passenger(
        name=name,
        passport_number=f"{name.upper()}_PASS123",
        email=f"{name.lower()}@example.com",
        join_date=datetime.utcnow(),
    )
    test_db.add(passenger)
    test_db.commit()
    test_db.refresh(passenger)
    return passenger


def test_pricing_rules(test_db, setup_data):
    service = BookingService(test_db)
    flight = setup_data["flight"]
    seat = setup_data["seat"]

    # Early booking (30+ days before departure)
    alice = create_passenger(test_db, "Alice")
    booking = service.create_booking(alice.id, flight.id, seat.id)
    assert booking.price <= flight.base_price  # early-bird discount

    # Late booking (within 7 days)
    # Move departure closer for late booking
    flight.departure_time = datetime.utcnow() + timedelta(days=5)
    test_db.commit()

    # Use another seat to avoid double-booking
    late_seat = FlightSeat(seat_code="1B", cabin_class="ECONOMY", flight_id=flight.id)
    test_db.add(late_seat)
    test_db.commit()
    test_db.refresh(late_seat)

    bob = create_passenger(test_db, "Bob")
    booking2 = service.create_booking(bob.id, flight.id, late_seat.id)
    assert booking2.price >= flight.base_price  # late-booking surcharge


def test_cannot_double_book_same_seat(test_db, setup_data):
    service = BookingService(test_db)
    flight = setup_data["flight"]
    seat = setup_data["seat"]

    alice = create_passenger(test_db, "Alice")
    booking = service.create_booking(alice.id, flight.id, seat.id)
    assert booking is not None

    bob = create_passenger(test_db, "Bob")
    with pytest.raises(Exception):
        service.create_booking(bob.id, flight.id, seat.id)


def test_hold_expiration_cancels_booking(test_db, setup_data):
    service = BookingService(test_db)
    flight = setup_data["flight"]
    seat = setup_data["seat"]

    alice = create_passenger(test_db, "Alice")
    booking = Booking(
        passenger_id=alice.id,
        flight_id=flight.id,
        flight_seat_id=seat.id,
        status="HELD",
        hold_expires_at=datetime.utcnow() - timedelta(minutes=1),  # already expired
    )
    test_db.add(booking)
    test_db.commit()

    # Expire holds
    service.expire_holds()

    test_db.refresh(booking)
    assert booking.status == "CANCELLED"
