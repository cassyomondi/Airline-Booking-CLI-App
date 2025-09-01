# test_queries.py
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from database import Base
from models.flight import Flight
from models.passenger import Passenger
from models.flight_seat import FlightSeat
from models.booking import Booking

# --- Setup DB ---
engine = create_engine("sqlite:///airline.db", echo=False, future=True)


def run_queries():
    session = Session(bind=engine)

    print("\n--- 1. List all bookings for a passenger ---")
    passenger = session.execute(
        select(Passenger).where(Passenger.name == "Alice Kimani")
    ).scalar_one()
    print(f"Passenger: {passenger.name}")
    for booking in passenger.bookings:
        print(f"  Booking #{booking.id}: Flight {booking.flight.flight_number}, "
              f"Seat {booking.flight_seat.seat_code}, "
              f"Status={booking.status}, Price={booking.price}")

    print("\n--- 2. List all seats for a flight (booked vs available) ---")
    flight = session.execute(
        select(Flight).where(Flight.flight_number == "KQ101")
    ).scalar_one()
    print(f"Flight: {flight.flight_number} {flight.origin} -> {flight.destination}")
    for seat in flight.seats:
        booking = seat.booking  # relationship (if defined one-to-one)
        if booking:
            print(f"  Seat {seat.seat_code} ({seat.cabin_class}) -> BOOKED by {booking.passenger.name}")
        else:
            print(f"  Seat {seat.seat_code} ({seat.cabin_class}) -> AVAILABLE")

    print("\n--- 3. Get passenger details from a booking ---")
    booking = session.execute(select(Booking).limit(1)).scalar_one()
    print(f"Booking #{booking.id} is for passenger {booking.passenger.name}, "
          f"Flight {booking.flight.flight_number}, Seat {booking.flight_seat.seat_code}")

    session.close()


if __name__ == "__main__":
    run_queries()
