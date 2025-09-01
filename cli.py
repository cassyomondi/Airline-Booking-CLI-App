# cli.py
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from database import Base
from models.flight import Flight
from models.passenger import Passenger
from models.flight_seat import FlightSeat
from models.booking import Booking

engine = create_engine("sqlite:///airline.db", echo=False, future=True)


def view_flights(session: Session):
    flights = session.scalars(select(Flight)).all()
    if not flights:
        print("No flights available.")
    else:
        for f in flights:
            print(f"ID: {f.id} | Flight: {f.flight_number} | {f.origin} → {f.destination} "
                  f"| Departs: {f.departure_time} | Arrives: {f.arrival_time} | Capacity: {f.capacity}")


def view_passengers(session: Session):
    passengers = session.scalars(select(Passenger)).all()
    if not passengers:
        print("No passengers found.")
    else:
        for p in passengers:
            print(f"ID: {p.id} | Name: {p.name} | Email: {p.email} | Passport: {p.passport_number}")


def add_passenger(session: Session):
    name = input("Enter passenger name: ")
    email = input("Enter email: ")
    passport_number = input("Enter passport number: ")

    passenger = Passenger(name=name, email=email, passport_number=passport_number)
    session.add(passenger)
    session.commit()
    print(f"Passenger {name} added successfully with ID {passenger.id}")


def delete_passenger(session: Session):
    passenger_id = input("Enter Passenger ID to delete: ")
    passenger = session.get(Passenger, passenger_id)

    if not passenger:
        print("Passenger not found.")
        return

    # Delete associated bookings first
    bookings = session.scalars(select(Booking).where(Booking.passenger_id == passenger.id)).all()
    for booking in bookings:
        session.delete(booking)

    session.delete(passenger)
    session.commit()
    print(f"Passenger {passenger.name} (ID {passenger.id}) and their bookings have been deleted.")


def book_seat(session: Session):
    passenger_email = input("Enter passenger email: ")
    passenger = session.scalar(select(Passenger).where(Passenger.email == passenger_email))

    if not passenger:
        print("Passenger not found. Please Confirm if the passenger is registered.")
        return

    view_flights(session)
    flight_id = input("Enter Flight ID to book: ")
    flight = session.get(Flight, flight_id)
    if not flight:
        print("Invalid flight ID.")
        return

    available_seats = session.scalars(
        select(FlightSeat).where(
            FlightSeat.flight_id == flight.id,
            FlightSeat.id.not_in(select(Booking.flight_seat_id))
        )
    ).all()

    if not available_seats:
        print("No seats available for this flight.")
        return

    print("\nAvailable Seats:")
    for seat in available_seats:
        print(f"{seat.id}: {seat.seat_code} ({seat.cabin_class})")

    seat_id = input("Enter Seat ID to book: ")
    seat = session.get(FlightSeat, seat_id)
    if not seat:
        print("Invalid seat selection.")
        return

    booking = Booking(
        passenger_id=passenger.id,
        flight_id=flight.id,
        flight_seat_id=seat.id,
        price=flight.base_price,
        status="CONFIRMED"
    )
    session.add(booking)
    session.commit()
    print(f"Seat {seat.seat_code} booked for {passenger.name} on flight {flight.flight_number}")


def view_bookings(session: Session):
    bookings = session.scalars(select(Booking)).all()
    if not bookings:
        print("No bookings found.")
    else:
        for b in bookings:
            passenger = session.get(Passenger, b.passenger_id)
            flight = session.get(Flight, b.flight_id)
            seat = session.get(FlightSeat, b.flight_seat_id)
            print(f"Booking ID: {b.id} | Passenger: {passenger.name} | Flight: {flight.flight_number} "
                  f"| Seat: {seat.seat_code} | Status: {b.status}")


def cancel_booking(session: Session):
    booking_id = input("Enter Booking ID to cancel: ")
    booking = session.get(Booking, booking_id)
    if not booking:
        print("Booking not found.")
        return

    booking.status = "CANCELLED"
    session.commit()
    print(f"Booking {booking_id} cancelled.")


def main_menu():
    with Session(bind=engine) as session:
        while True:
            print("\n--- Airline Booking CLI ---")
            print("1. View Flights")
            print("2. View Passengers")
            print("3. Add Passenger")
            print("4. Delete Passenger")
            print("5. Book a Seat")
            print("6. View Bookings")
            print("7. Cancel Booking")
            print("8. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                view_flights(session)
            elif choice == "2":
                view_passengers(session)
            elif choice == "3":
                add_passenger(session)
            elif choice == "4":
                delete_passenger(session)
            elif choice == "5":
                book_seat(session)
            elif choice == "6":
                view_bookings(session)
            elif choice == "7":
                cancel_booking(session)
            elif choice == "8":
                print("Thank you for using the Airline Booking CLI. Goodbye!")
                break
            else:
                print("Invalid choice, try again.")


if __name__ == "__main__":
    main_menu()
